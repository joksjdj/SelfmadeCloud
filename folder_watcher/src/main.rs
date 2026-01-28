use watcher::{print_test, Time};

fn main() {
    let t = Time::run();
    
    t(|| print_test("Hello from lib.rs"));
}