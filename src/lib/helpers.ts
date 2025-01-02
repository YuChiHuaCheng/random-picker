import { join } from "path";
import pl, { type DataFrame, Float64, Series, Utf8 } from "nodejs-polars";

const filepath = join(import.meta.dirname, "merged_douban.csv");
export const df = pl.readCSV(filepath, { quoteChar: '""' }) as DataFrame<{
  Item_name: Series<Utf8, "Item_name">;
  Genres: Series<Utf8, "Genres">;
  Score: Series<Float64, "Score">;
  Type: Series<Utf8, "Type">;
}>;

export const getGenres = (type: string) => {
  const filteredDf = df.filter(pl.col("Type").eq(pl.lit(type)));
  const genres = filteredDf
    .select("Genres")
    .dropNulls()
    .unique()
    .toSeries()
    .toArray() as string[];
  return genres;
};
