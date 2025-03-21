const App = {
    template: `
      <div class="min-h-screen flex items-center justify-center bg-gray-100">
        <div class="bg-white shadow rounded-lg p-6 w-80">
          <h1 class="text-xl font-bold mb-4">Recherche</h1>
          <form @submit.prevent="search">
            <div class="mb-4">
              <input
                v-model="query"
                type="text"
                placeholder="Entrez votre recherche"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button
              type="submit"
              class="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            >
              Rechercher
            </button>
          </form>
          <div v-if="loading" class="mt-4 text-gray-600">Recherche en cours...</div>
          <div v-if="results" class="mt-4">
            <h2 class="text-lg font-semibold">Résultats :</h2>
            <ul class="mt-2 space-y-2">
              <li v-for="(result, index) in results" :key="index" class="bg-gray-100 p-2 rounded">
                {{ result }}
              </li>
            </ul>
          </div>
          <div v-if="error" class="mt-4 text-red-500">Erreur : {{ error }}</div>
        </div>
      </div>
    `,
    data() {
      return {
        query: "",
        results: null,
        loading: false,
        error: null,
      };
    },
    methods: {
      async search() {
        this.loading = true;
        this.results = null;
        this.error = null;
  
        try {
          const response = await fetch(`https://api.example.com/search?q=${encodeURIComponent(this.query)}`);
          if (!response.ok) {
            throw new Error("Erreur lors de la recherche");
          }
          const data = await response.json();
          this.results = data.results;
        } catch (err) {
          this.error = err.message;
        } finally {
          this.loading = false;
        }
      },
    },
  };
  
  Vue.createApp(App).mount('#app');
  