import pandas as pd


def retrieve_relevant_data(df, question):
    """
    Generic retrieval layer that works across
    multiple CSV schemas.
    """

    q = question.lower()
    temp_df = df.copy()

    numeric_cols = temp_df.select_dtypes(include="number").columns.tolist()

    text_cols = [c for c in temp_df.columns if c not in numeric_cols]

    # -------------------
    # Highest
    # -------------------
    if any(word in q for word in ["highest", "best", "top", "maximum"]):

        if numeric_cols:
            metric = numeric_cols[0]

            return temp_df.nlargest(min(5, len(temp_df)), metric)

    # -------------------
    # Lowest
    # -------------------
    if any(word in q for word in ["lowest", "worst", "minimum"]):

        if numeric_cols:
            metric = numeric_cols[0]

            return temp_df.nsmallest(min(5, len(temp_df)), metric)

    # -------------------
    # Average
    # -------------------
    if any(word in q for word in ["average", "mean"]):

        rows = []

        for col in numeric_cols:

            rows.append({"metric": col, "average": round(temp_df[col].mean(), 2)})

        return pd.DataFrame(rows)

    # -------------------
    # Total
    # -------------------
    if any(word in q for word in ["total", "sum"]):

        rows = []

        for col in numeric_cols:

            rows.append({"metric": col, "total": round(temp_df[col].sum(), 2)})

        return pd.DataFrame(rows)

    # -------------------
    # Growth / Trend
    # -------------------
    if any(word in q for word in ["growth", "trend"]):

        result = temp_df.copy()

        for col in numeric_cols:

            result[f"{col}_growth_pct"] = (result[col].pct_change() * 100).round(2)

        return result

    # -------------------
    # Column Search
    # -------------------
    for col in text_cols:

        values = temp_df[col].astype(str).str.lower().unique()

        for val in values:

            if val in q:

                return temp_df[temp_df[col].astype(str).str.lower() == val]

    return temp_df
