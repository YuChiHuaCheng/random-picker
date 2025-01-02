import { error, json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { getGenres } from "$lib/helpers";

export const GET: RequestHandler = ({ url }) => {
  const type = url.searchParams.get("type");

  if (!type) {
    error(400, "请选择类型");
  }

  const genres = getGenres(type);

  return json({ genres });
};
