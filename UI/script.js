async function submitForm(event) {
    event.preventDefault();

    const inputField = document.getElementById('inputField');
    const inputValue = inputField.value;

    const apiUrl = `https://6qvqst6ja4.execute-api.eu-west-3.amazonaws.com/dev/search-artist?query=${encodeURIComponent(inputValue)}`;
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('Réponse de l\'API:', responseData);
        //alert('Données récupérées avec succès !');
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<pre>${JSON.stringify(responseData, null, 2)}</pre>`;
    } catch (error) {
        console.error('Erreur lors de la requête API:', error);
        alert('Une erreur est survenue lors de la récupération des données.');
    }
}
