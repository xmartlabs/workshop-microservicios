#[macro_use]
extern crate rocket;

use std::fmt::Write;

use futures::stream::StreamExt;
use rocket_db_pools::mongodb;
use rocket_db_pools::mongodb::bson::{doc, Document};
use rocket_db_pools::{Connection, Database};

#[derive(Database)]
#[database("balance")]
struct MongoDB(mongodb::Client);

#[post("/insert")]
async fn insert(db: Connection<MongoDB>) {
    let collection = db.database("balances").collection::<Document>("books");

    let docs = vec![
        doc! { "title": "1984", "author": "George Orwell" },
        doc! { "title": "Animal Farm", "author": "George Orwell" },
        doc! { "title": "The Great Gatsby", "author": "F. Scott Fitzgerald" },
    ];

    collection.insert_many(docs, None).await.unwrap();
}

#[get("/list")]
async fn list(db: Connection<MongoDB>) -> String {
    let collection = db.database("balance").collection::<Document>("books");

    let mut return_value = String::new();
    let mut cursor = collection.find(None, None).await.unwrap();
    while let Some(result) = cursor.next().await {
        if let Ok(document) = result {
            write!(&mut return_value, "{}", document).unwrap();
        }
    }

    return_value
}

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(MongoDB::init())
        .mount("/", routes![index, insert, list])
}
