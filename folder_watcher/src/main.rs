use watcher::{print_test, Time, check_files};
use std::path::Path;
use std::fs::File;
use std::io::{Read, Write}; 
use std::net::{TcpListener, TcpStream};

fn main() {
    let t = Time::run();
    
    t(|| print_test("Hello from lib.rs"));

    let path = Path::new("data/cloud");

    if path.exists() {
        println!("Data folder exists!");
    } else {
        println!("Data folder missing!");
    }

    check_files();

    let listener = TcpListener::bind("172.30.31.51:9000").unwrap(); 
    println!("TCP server on 9000");

    for stream in listener.incoming() { 
        let mut stream = stream.unwrap(); 
        let mut file = File::open("data/sendFiles/test.txt").unwrap(); 
        let mut buf = [0u8; 4096];

        loop { 
            let n = file.read(&mut buf).unwrap(); 
            if n == 0 { break; } 
            stream.write_all(&buf[..n]).unwrap(); 
        } 
        println!("File received."); 
    }

}