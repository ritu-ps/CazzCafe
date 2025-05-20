async function getOrders() {
    try {
        const response = await fetch('http://localhost:5000/api/orders');
        const orders = await response.json();
        console.log('Orders:', orders);
        return orders;
    } catch (error) {
        console.error('Error fetching orders:', error);
        return [];
    }
}