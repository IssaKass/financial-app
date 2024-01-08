import { useState } from "react";
import "./App.css";

function App() {
	const [number, setNumber] = useState(0);

	console.log(import.meta.env.MODE);
	console.log(import.meta.env.BASE_URL);
	console.log(import.meta.env.PROD);
	console.log(import.meta.env.DEV);
	console.log(import.meta.env.SSR);
	console.log(import.meta.env.VITE_APP_TITLE);
	console.log(import.meta.env.VITE_API_URL);

	const handleClick = () => {
		fetch("/api")
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
