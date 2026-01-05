import Toc from "./Toc";
import { sections } from "./sections";


export default function App() {
    return (
        <>
            <Toc />
            {sections.map(s => (
                <section id={s.id} key={s.id} className="page">
                    <h1>{s.title}</h1>
                    <p>내용 더미 영역</p>
                </section>
            ))}
        </>
    );
}

// 테스트용
useEffect(() => {
  fetchResearch().then(console.log);
}, []);