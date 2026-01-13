export async function fetchResearch() {
  const res = await fetch("http://localhost:8080/api/research");
  return res.json();
}
