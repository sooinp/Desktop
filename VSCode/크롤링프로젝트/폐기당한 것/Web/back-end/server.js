import express from "express";
import cors from "cors";
import researchRouter from "./routes/research.js";


const app = express();
app.use(cors());
app.use(express.json());


app.use("/api/research", researchRouter);


app.listen(8080, () => {
    console.log("Server running on port 8080");
});