const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;

const client = redis.createClient();

client.on('error', (err) => {
    console.error(`Error: ${err}`);
});

const getAsync = promisify(client.get).bind(client);

const listProducts = [
    { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
    { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

function getItemById(id) {
    return listProducts.find((item) => item.id === id);
}

async function reserveStockById(id) {
    const item = getItemById(id);
    if (item && item.stock > 0) {
        item.stock -= 1;

        await client.set(`item.${id}`, item.stock);
        return true;
    }
    return false;
}

async function getCurrentReservedStockById(itemId) {
    const value = await getAsync(`item.${itemId}`);
    return value !== null ? parseInt(value, 10) : 0;
}

app.get('/list_products', (_, res) => {
    const formattedProducts = listProducts.map(item => ({
        itemId: item.id,
        itemName: item.name,
        price: item.price,
        initialAvailableQuantity: item.stock
    }));
    res.json(formattedProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const item = getItemById(itemId);

    if (item) {
        const currentQuantity = await getCurrentReservedStockById(itemId);
        res.json({
            itemId: item.id,
            itemName: item.name,
            price: item.price,
            initialAvailableQuantity: item.stock,
            currentQuantity: currentQuantity
        });
    } else {
        res.status(404).json({ status: 'Product not found' });
    }
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const item = getItemById(itemId);

    if (!item) {
        return res.status(404).json({ status: 'Product not found' });
    }

    if (item.stock <= 0) {
        return res.status(400).json({ status: 'Not enough stock available', itemId: item.id });
    }

    const reserved = await reserveStockById(itemId);
    if (reserved) {
        res.json({ status: 'Reservation confirmed', itemId: item.id });
    } else {
        res.status(400).json({ status: 'Not enough stock available', itemId: item.id });
    }
});

app.listen(port, () => {
    console.log(`Server is listening on port ${port}`);
});
