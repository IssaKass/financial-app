import { useState } from "react";
import "./App.css";

function App() {
	const [number, setNumber] = useState(0);

	const handleClick = () => {
		fetch("/api/")
			.then((res) => res.json())
			.then((data) => setNumber(data.number))
			.catch((error) => console.error(error));
	};

	return (
		<>
			<button onClick={handleClick}>Fetch Data</button>
			<p>{number}</p>
		</>
	);
}

export default App;
