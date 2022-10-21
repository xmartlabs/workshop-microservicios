#[macro_use]
extern crate rocket;

use futures::stream::StreamExt;
use rocket::serde::{json::Json, Deserialize, Serialize};
use rocket_db_pools::mongodb::{
    self,
    bson::{self, doc},
};
use rocket_db_pools::{Connection, Database};

const DEFAULT_BALANCE_AMOUNT: f64 = 1000.0;

#[derive(Database)]
#[database("main")]
struct MongoDB(mongodb::Client);

#[get("/databases")]
async fn list_databases(db: Connection<MongoDB>) -> String {
    let databases = db.list_database_names(None, None).await.unwrap();

    format!("{:?}", databases)
}

#[derive(Deserialize)]
#[serde(crate = "rocket::serde")]
struct MoneyMovement<'r> {
    customer_id: &'r str,
    amount: f64,
}

#[derive(Serialize)]
#[serde(crate = "rocket::serde")]
struct MoneyMovementResponse {
    amount: f64,
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(crate = "rocket::serde")]
struct Balance {
    customer_id: String,
    amount: f64,
}

#[post("/register", data = "<money_movement>")]
async fn register(
    money_movement: Json<MoneyMovement<'_>>,
    db: Connection<MongoDB>,
) -> Json<MoneyMovementResponse> {
    let balances = db.database("main").collection::<Balance>("balances");
    let customer_balance = balances
        .find_one(doc! { "customer_id": money_movement.customer_id }, None)
        .await
        .expect("Could not fetch customer balance");

    let new_balance = match customer_balance {
        None => {
            let new_amount = DEFAULT_BALANCE_AMOUNT + money_movement.amount;

            if new_amount < 0.0 {
                panic!("Not enough money!");
            }

            let new_balance = Balance {
                customer_id: money_movement.customer_id.to_owned(),
                amount: new_amount,
            };

            balances.insert_one(new_balance, None).await.unwrap();

            Json(MoneyMovementResponse { amount: new_amount })
        }
        Some(old_balance) => {
            let amount = old_balance.amount;
            let new_amount = amount + money_movement.amount;

            if new_amount < 0.0 {
                panic!("Not enough money!");
            }

            let bson = bson::to_bson(&old_balance).unwrap();
            let document = bson.as_document().unwrap();

            balances
                .update_one(
                    document.to_owned(),
                    doc! { "$set": { "amount": new_amount } },
                    None,
                )
                .await
                .unwrap();

            Json(MoneyMovementResponse { amount: new_amount })
        }
    };

    new_balance
}

#[get("/balances")]
async fn list_balances(db: Connection<MongoDB>) -> String {
    let balances_collection = db.database("main").collection::<Balance>("balances");

    let balances: Vec<_> = balances_collection
        .find(None, None)
        .await
        .unwrap()
        .collect()
        .await;

    format!("{:?}", balances)
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(MongoDB::init())
        .mount("/", routes![list_databases, register, list_balances])
}
