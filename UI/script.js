new Vue({
    el: '#app',
    data: {
        inputValue: '',
        responseData: null,
        errorMessage: ''
    },
    methods: {
        async submitForm() {
            const apiUrl = `https://allmusicgrabber.azurewebsites.net/api/search-artist?query=${encodeURIComponent(this.inputValue)}`;
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

                this.responseData = await response.json();
                this.errorMessage = '';
            } catch (error) {
                console.error('Erreur lors de la requête API:', error);
                this.errorMessage = 'Une erreur est survenue lors de la récupération des données.';
                this.responseData = null;
            }
        }
    }
});
