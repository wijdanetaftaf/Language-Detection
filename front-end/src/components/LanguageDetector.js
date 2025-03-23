import React, { useState } from "react";
import "../style.css"; // Importer le CSS

const LanguageDetector = () => {
    const [text, setText] = useState("");
    const [language, setLanguage] = useState(null);
    const [loading, setLoading] = useState(false);

    const detectLanguage = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:5000/detect", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text }),
            });

            const data = await response.json();
            setLanguage(data.language);
        } catch (error) {
            console.error("Erreur lors de la requête:", error);
            alert("Erreur lors de la connexion à l'API.");
        }

        setLoading(false);
    };

    return (
        <div className="background-video">
            {/* Vidéo de fond */}
            <video autoPlay loop muted className="background-video">
                <source src="best.mp4" type="video/mp4" />
                Votre navigateur ne prend pas en charge la vidéo.
            </video>

            {/* Contenu principal */}
            <div className="content">
                <h1>Détection de Langue</h1>
                <form onSubmit={detectLanguage}>
                    <textarea
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Entrez un texte ici..."
                        required
                    />
                    <br />
                    <button type="submit" disabled={loading}>
                        {loading ? "Détection en cours..." : "Détecter"}
                    </button>
                </form>

                {/* Affichage du résultat */}
                {language && (
                    <div className="result">
                        <h3>Langue détectée :</h3>
                        <p><strong>Langue :</strong> {language}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default LanguageDetector;
