import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from classify import classify

app = FastAPI(title="AI Log Classification API")
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Serve CSS and JavaScript
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home page
@app.get("/")
async def home():
    return FileResponse("static/index.html")

# CSV Classification API
@app.post("/classify/")
async def classify_logs(file: UploadFile):
    # Validate file extension
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="File must be a CSV."
        )

    try:
        # Read uploaded CSV
        df = pd.read_csv(file.file)

        # Validate required columns
        required_columns = {"source", "log_message"}

        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'source' and 'log_message' columns."
            )

        # Perform classification
        df["target_label"] = classify(
            list(zip(df["source"], df["log_message"]))
        )

        # Save output CSV
        output_file = "resources/output.csv"
        df.to_csv(output_file, index=False)

        # Return classified CSV
        return FileResponse(
            path=output_file,
            filename="output.csv",
            media_type="text/csv"
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        file.file.close()