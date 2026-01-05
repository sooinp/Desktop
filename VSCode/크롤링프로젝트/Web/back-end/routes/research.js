import express from "express";
import { pool } from "../db.js";


const router = express.Router();


router.get("/", async (req, res) => {
    const [rows] = await pool.query("SELECT * FROM defense_research");
    res.json(rows);
    res.send("정상 동작");
});


export default router;