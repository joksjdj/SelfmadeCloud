use watcher::{print_test, Time};
use std::path::Path;

fn main() {
    let t = Time::run();
    
    t(|| print_test("Hello from lib.rs"));

    let path = Path::new("data");

    if path.exists() {
        println!("Data folder exists!");
    } else {
        println!("Data folder missing!");
    }

}