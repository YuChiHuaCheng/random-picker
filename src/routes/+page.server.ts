import { superValidate, message } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";

import type { Actions, PageServerLoad } from "./$types";
import { schema } from "./schema";
import { getSampleOne, getTypes } from "$lib/server/helper";
import { fail } from "@sveltejs/kit";

export const load: PageServerLoad = async () => {
  const types = getTypes();

  return {
    form: await superValidate(zod(schema)),
    types,
  };
};

export const actions = {
  default: async ({ request }) => {
    const regForm = await superValidate(request, zod(schema));

    if (!regForm.valid) return fail(400, { regForm });

    const random = getSampleOne({
      ...regForm.data,
      score: regForm.data.score ?? 0,
    });

    return message(regForm, { random });
  },
} satisfies Actions;
