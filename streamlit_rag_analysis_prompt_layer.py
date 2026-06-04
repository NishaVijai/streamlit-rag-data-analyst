import pandas as pd

def retrieve_relevant_data(df, question):

    q = question.lower()

    # Work on copy
    temp_df = df.copy()

    months = [
        "jan", "feb", "mar",
        "apr", "may", "jun"
    ]

    # -------------------
    # Highest Sales
    # -------------------
    if "highest" in q or "best" in q:
        return temp_df.nlargest(3, "sales")

    # -------------------
    # Lowest Sales
    # -------------------
    elif "lowest" in q or "worst" in q:
        return temp_df.nsmallest(3, "sales")

    # -------------------
    # Average Sales
    # -------------------
    elif "average" in q or "mean" in q:
        return pd.DataFrame({
            "metric": ["Average Sales"],
            "value": [temp_df["sales"].mean()]
        })

    # -------------------
    # Total Sales
    # -------------------
    elif "total" in q or "sum" in q:
        return pd.DataFrame({
            "metric": ["Total Sales"],
            "value": [temp_df["sales"].sum()]
        })

    # -------------------
    # Growth Analysis
    # -------------------
    elif "growth" in q or "trend" in q:

        temp_df["growth_pct"] = (
            temp_df["sales"]
            .pct_change() * 100
        ).round(2)

        return temp_df

    # -------------------
    # Specific Month Search
    # -------------------
    elif any(month in q for month in months):

        for month in months:

            if month in q:

                return temp_df[
                    temp_df["month"]
                    .str.lower() == month
                ]

    # -------------------
    # Fallback
    # -------------------
    return temp_df