import { z } from "zod";

export const schema = z.object({
  type: z.string().min(1),
  genre: z.string().min(1),
  score: z.number().min(0).default(0),
});
