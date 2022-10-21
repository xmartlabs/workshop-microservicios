FROM rust:1.63 as build

RUN USER=root cargo new --bin balance

WORKDIR /balance

COPY ./Cargo.lock ./Cargo.lock
COPY ./Cargo.toml ./Cargo.toml

RUN cargo build
RUN rm src/*.rs

COPY ./Rocket.toml ./Rocket.toml
COPY ./src ./src

RUN rm ./target/debug/deps/balance*
RUN cargo build

CMD ["cargo", "run"]
