// server.js
const express = require('express');
const {
  ProfileNetworthCalculator,
  // Optional helpers you might use later:
  // NetworthManager, getPrices
} = require('skyhelper-networth');

const app = express();
const port = process.env.PORT || 5000;

app.use(express.json({ limit: '20mb' }));


app.post('/networth', async (req, res) => {
  try {
    const { profile, bank, museumData } = req.body;

    const calc = new ProfileNetworthCalculator(profile, museumData, bank);

    const networth = await calc.getNetworth({
    });

    res.send(networth);
  } catch (err) {
    res.status(400).send(err?.message || 'Failed to compute networth');
  }
});

app.listen(port, () => {
  console.log(`Running on port ${port}`);
});

