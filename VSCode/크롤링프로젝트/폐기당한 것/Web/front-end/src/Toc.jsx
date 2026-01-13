import { sections } from "./sections";


export default function Toc() {
    const move = (id) => {
    document.getElementById(id).scrollIntoView({ behavior: "smooth" });
    };

    return (
        <div className="toc">
            {sections.map(s => (
                <div key={s.id} onClick={() => move(s.id)}>
                    {s.title}
                </div>
            ))}
        </div>
    );
}