import pl from "nodejs-polars";
import type { DataFrame, Float64, Series, Utf8 } from "nodejs-polars";
import csvData from "../../merged_douban.csv?raw";

export const df = pl.readCSV(csvData, { quoteChar: '""' }) as DataFrame<{
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

export const getTypes = () => {
  return df
    .select("Type")
    .dropNulls()
    .unique()
    .toSeries()
    .toArray() as string[];
};

type Params = {
  type: string;
  genre: string;
  score: number;
};

export type Resource = {
  Item_name: string;
  Genres: string;
  Score: number;
  Type: string;
};

export const getSampleOne = ({ type, genre, score }: Params) => {
  const filteredDf = df
    .filter(pl.col("Score").gtEq(score))
    .filter(pl.col("Genres").eq(pl.lit(genre)))
    .filter(pl.col("Type").eq(pl.lit(type)));

  if (filteredDf.isEmpty()) {
    return null;
  }

  const random = filteredDf.sample(1).toDataResource().data as [Resource];

  return random;
};
