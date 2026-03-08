new Vue({
    el: '#app',
    data: {
        inputValue: '',
        responseData: null,
        errorMessage: ''
    },
    methods: {
        async submitForm() {
            const apiUrl = `https://allmusicgrabber.azurewebsites.net/api/find-artist?query=${encodeURIComponent(this.inputValue)}`;
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
                this.$nextTick(() => {
                    this.drawDiscographyChart();
                });
            } catch (error) {
                console.error('Erreur lors de la requête API:', error);
                this.errorMessage = 'Une erreur est survenue lors de la récupération des données.';
                this.responseData = null;
            }
        },

        drawDiscographyChart() {
            if (!this.responseData || !this.responseData.discography) return;

            const rawData = this.responseData.discography
                .filter(d => d.albumYear && d.musicRating !== null && d.musicRating !== undefined);

            if (!rawData.length) return;

            // Transforme les données pour D3
            const data = rawData.map(d => ({
                album: d.albumTitle,
                year: +d.albumYear,
                note: +d.musicRating
            }));

            // Nettoyer le conteneur si on redessine
            d3.select('#discography-chart').selectAll('*').remove();

            const margin = { top: 40, right: 150, bottom: 60, left: 60 },
                  width  = 800 - margin.left - margin.right,
                  height = 400 - margin.top - margin.bottom;

            const svg = d3.select('#discography-chart')
                .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            const x = d3.scaleLinear()
                .domain(d3.extent(data, d => d.year))
                .range([0, width]);

            const y = d3.scaleLinear()
                .domain([
                    d3.min(data, d => d.note) - 0.5,
                    d3.max(data, d => d.note) + 0.5
                ])
                .range([height, 0]);

            const xAxis = d3.axisBottom(x)
                .ticks(data.length)
                .tickFormat(d3.format('d'));

            const yAxis = d3.axisLeft(y)
                .ticks(10);

            svg.append('g')
                .attr('class', 'd3-axis')
                .attr('transform', `translate(0,${height})`)
                .call(xAxis);

            svg.append('g')
                .attr('class', 'd3-axis')
                .call(yAxis);

            svg.append('text')
                .attr('text-anchor', 'middle')
                .attr('x', width / 2)
                .attr('y', height + margin.bottom - 15)
                .text('Année');

            svg.append('text')
                .attr('text-anchor', 'middle')
                .attr('transform', 'rotate(-90)')
                .attr('x', -height / 2)
                .attr('y', -margin.left + 15)
                .text('Note musique');

            const line = d3.line()
                .x(d => x(d.year))
                .y(d => y(d.note));

            svg.append('path')
                .datum(data)
                .attr('class', 'd3-line')
                .attr('d', line);

            svg.selectAll('.d3-circle')
                .data(data)
                .enter()
                .append('circle')
                .attr('class', 'd3-circle')
                .attr('cx', d => x(d.year))
                .attr('cy', d => y(d.note))
                .attr('r', 4);

            svg.selectAll('.d3-label')
                .data(data)
                .enter()
                .append('text')
                .attr('class', 'd3-label')
                .attr('x', d => x(d.year) + 5)
                .attr('y', d => y(d.note) - 5)
                .text(d => d.album)
                .attr('transform', d => `rotate(-30, ${x(d.year) + 5}, ${y(d.note) - 5})`);
        }
    }
});
