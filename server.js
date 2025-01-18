const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public')); // Serve static files (HTML, JS)

async function fetchLinks(query) {
    try {
        const response = await axios.get(`https://www.google.com/search?q=${encodeURIComponent(query)}`);
        const $ = cheerio.load(response.data);
        const links = [];
        
        // Scrape Google search results (extract <a> tags)
        $('a').each((i, elem) => {
            const url = $(elem).attr('href');
            if (url && url.startsWith('http')) {
                links.push(url);
            }
        });
        
        return links;
    } catch (error) {
        console.error('Error fetching search results:', error);
        return [];
    }
}

app.get('/search', async (req, res) => {
    const { query } = req.query;
    const links = await fetchLinks(query);
    res.json(links);
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
