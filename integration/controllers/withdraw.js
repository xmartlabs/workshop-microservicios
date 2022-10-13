
module.exports = {
    withdraw: (req, res) => {
        const customer_id = req.body.customer_id;
        const account = req.body.account;
        const amount = req.body.amount;
        if (amount < 50) {
            res.status(500);
            res.send('Internal Server Error');
        }  else if (amount > 100) {
            res.status(200);
            res.send(`Transferred $${amount} from account ${account} of client ${customer_id}`);
        } 
    },
};
