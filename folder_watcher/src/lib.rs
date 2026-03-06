use colored::*;
use std::fs;

pub struct Time;
impl Time {
    pub fn run() -> impl Fn(fn()) {
        move |f: fn()| {
            let start = std::time::Instant::now();
            f();
            let duration = start.elapsed();
            let ms = (duration.as_secs_f64() * 1000.0).ceil() / 1000.0;
            println!("Time elapsed: {:.3} ms\n", ms);
        }
    }
}

pub fn print_test(text: &str) {
    println!("\n{}", text.to_string().purple());
}

pub fn check_files() {
    let look_files = fs::read_dir("data/cloud/files").unwrap();

    for files in look_files {
        println!("Name: {}", files.unwrap().path().display());
    }
}