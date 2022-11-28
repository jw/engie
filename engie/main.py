import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Entries(BaseModel):
    data: list[str]


def converter(entries: list[str]) -> list:
    """
    Convert the entries: when the `ord(str)` is lower than `ord("H")` or `ord("h")`,
    `ord(str) * 10` is returned, otherwise `0` is returned.

    :param entries: A list of characters.
    :return: The converted list of numbers
    """
    df = pd.DataFrame(entries, columns=["data"])
    ord_df = df.applymap(ord)
    ord_array = ord_df["data"].values
    converted = np.where(
        (ord_array >= ord("H")) | (ord_array >= ord("h")), 0, ord_array * 10
    )
    return converted.tolist()


@app.post("/convert")
async def convert(entries: Entries) -> dict:
    return {"result": converter(entries.data)}


if __name__ == "__main__":
    uvicorn.run("engie.main:app", host="0.0.0.0", port=8000, reload=True)
