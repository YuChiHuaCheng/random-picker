import { df } from "$lib/helpers";
import { pl } from "nodejs-polars";
import { z } from "zod";
import type { Actions, PageServerLoad } from "./$types";
import { fail } from "@sveltejs/kit";

export const load: PageServerLoad = async () => {
  const types = df
    .select("Type")
    .dropNulls()
    .unique()
    .toSeries()
    .toArray() as string[];

  return { types } as { types: string[] };
};

const FormData = z.object({
  type: z.string(),
  genre: z.string(),
  score: z.preprocess((v) => Number(v), z.number()),
});

export const actions: Actions = {
  default: async ({ request }) => {
    const data = await request.formData();

    try {
      const parsed = FormData.parse(Object.fromEntries(data));
      const filteredDf = df.filter(
        pl
          .col("Type")
          .eq(pl.lit(parsed.type))
          .and(pl.col("Genres").eq(pl.lit(parsed.genre)))
          .and(pl.col("Score").gt(parsed.score))
      );
      const random = filteredDf.sample(1).toSeries().toArray();

      if (random.length === 0) {
        return fail(400, { missing: true });
      }

      return { success: true, data: { type: parsed.type, name: random[0] } };
    } catch {
      return fail(400, { missing: true });
    }
  },
};
