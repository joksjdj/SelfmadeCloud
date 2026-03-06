use watcher::{print_test, Time};
use std::path::Path;
use std::fs::File;
use std::io::{Read, Write};
use std::net::{TcpStream, TcpListener};

fn main() {
    let t = Time::run();
    
    t(|| print_test("Hello from lib.rs"));

    let path = Path::new("data");

    if path.exists() {
        println!("Data folder exists!");
    } else {
        println!("Data folder missing!");
    }

    let mut stream = TcpStream::connect("172.30.31.51:9000").expect("Could not connect.");

    let mut file = File::create("recieved.txt").expect("Could not create file.");

    let mut buf = [0u8; 4096];

    loop {
        let bytes_read = stream.read(&mut buf).expect("Failed to read from stream.");

        if bytes_read == 0 {
            break;
        }

        file.write_all(&buf[..bytes_read]).expect("Failed to write to file");
    }

    println!("File received");

}