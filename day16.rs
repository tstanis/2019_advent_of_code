use std::cmp;
use std::time::{Duration, Instant};
use std::collections::HashMap;

fn main() {
    let example0 = String::from("12345678");
    let example1 = String::from("80871224585914546619083218645595");
    let example2 = String::from("19617804207202209144916044189917");
    let example3 = String::from("03036732577212944063491565474664");
    let real = String::from("59708072843556858145230522180223745694544745622336045476506437914986923372260274801316091345126141549522285839402701823884690004497674132615520871839943084040979940198142892825326110513041581064388583488930891380942485307732666485384523705852790683809812073738758055115293090635233887206040961042759996972844810891420692117353333665907710709020698487019805669782598004799421226356372885464480818196786256472944761036204897548977647880837284232444863230958576095091824226426501119748518640709592225529707891969295441026284304137606735506294604060549102824977720776272463738349154440565501914642111802044575388635071779775767726626682303495430936326809");

    let origsignal: Vec<u32> = real
        .chars()
        .map(|s| s.to_digit(10).unwrap())
        .collect::<Vec<_>>();

    let mut cursignal: Vec<u32> = origsignal.clone();
    for i in 0..9999 {
        cursignal.extend(origsignal.clone())
    }
    println!("Orig Signal {} Expanded Signal {} {:?}", origsignal.len(), cursignal.len(), cursignal[0..64].to_vec());
    println!("Commence FFT");
    for i in 0..100 {
        let start_time = Instant::now();
        cursignal = compute_fft_phase_fast_runs(cursignal);
        println!("After {} in {:?}", i, start_time.elapsed());
    }
    let prefix = cursignal[0..20].to_vec();
    println!("Results {:?}", prefix);
    let mut offset : usize = 0;
    for i in 0..7 {
        offset = offset * 10 + (origsignal[i] as usize);
    }
    println!("Offset: {:?}", offset);
    let message : Vec<u32> = cursignal[offset..offset+8].to_vec();
    
    println!("Message: {:?}", message);
    let mut msgstring : usize = 0;
    for i in 0..8 {
        msgstring = msgstring * 10 + (message[i] as usize);
    }
    println!("MessageStr: {:?}", msgstring);
}

fn compute_fft_phase_fast(input_signal: Vec<u32>) -> Vec<u32> {
    let pattern = [0, 1, 0, -1];
    let input_signal_length = input_signal.len();
    //println!("Input Signal Length {}", input_signal_length);
    //println!(''.join(map(lambda x: str(x), input_signal[0:80])))
    let mut totals = vec![0u32; input_signal_length];

    //start = timer()
    let mut start = Instant::now();
    for line in 1..=input_signal_length {
        let mut cursor = 0;
        let mut total: i32 = 0;
        let mut first_cycle = true;
        while cursor < input_signal_length {
            //println!("Index {}", ((cursor+1) / line) % pattern.len());
            let coefficient = pattern[((cursor+1) / line) % pattern.len()];
            let mut num_to_process = cmp::min(line, input_signal_length - cursor);
            if first_cycle {
                num_to_process = if line > 1 {line - 1} else {1};
                first_cycle = false;
            }
            let thesum = input_signal[cursor..cursor+num_to_process].iter().sum::<u32>() as i32;
            if coefficient == 1 {
                total += thesum;
            } else if coefficient == -1 {
                total -= thesum;  
            }
            cursor += num_to_process;
            //println!("Total: {}", total);
        }
        totals[line - 1] = (i32::abs(total) % 10) as u32;
        if line % 100000 == 0 {
            println!("Totals {} time {:?}", line, start.elapsed() );
            start = Instant::now();
        }
    }
    return totals;
}

fn build_runs(input_signal: &Vec<u32>, run_size: usize) -> Vec<i32> {
    let mut runs: Vec<i32> = Vec::new();
    for line in (0..(input_signal.len()-run_size)+1) {
        runs.push(input_signal[line..line+run_size].iter().sum::<u32>() as i32);
    }
    return runs;
}

fn build_runs10x(input_signal: &Vec<u32>, input_runs: &Vec<i32>, input_run_size: usize, run_size: usize) -> Vec<i32> {
    let mut runs: Vec<i32> = Vec::new();
    let multiple = run_size / input_run_size;
    for line in (0..(input_signal.len()-run_size)+1) {
        let mut thesum = 0i32;
        for i in 0..multiple {
            thesum += input_runs[line+(input_run_size*i)]
        }
        runs.push(thesum);
    }
    return runs;
}

fn compute_fft_phase_fast_runs(input_signal: Vec<u32>) -> Vec<u32> {
    let pattern = [0, 1, 0, -1];
    let input_signal_length = input_signal.len();
    
    let mut totals = vec![0u32; input_signal_length];

    let mut start = Instant::now();
    let run_size = 100;
    let runs = build_runs(&input_signal, run_size);
    println!("Runs Build in {:?}", start.elapsed());
    let run_size_10x = run_size * 10;
    let runs10x = build_runs10x(&input_signal, &runs, run_size, run_size_10x);
    let run_size_100x = run_size * 100;
    let runs100x = build_runs10x(&input_signal, &runs10x, run_size_10x, run_size_100x);
    let run_size_1000x = run_size * 1000;
    let runs1000x = build_runs10x(&input_signal, &runs100x, run_size_100x, run_size_1000x);
    let mut run_hits = 0;
    println!("Runs 10x Build in {:?}", start.elapsed());
    start = Instant::now();
    for line in 1..=input_signal_length {
        let mut cursor = 0;
        let mut total: i32 = 0;
        let mut first_cycle = true;
        while cursor < input_signal_length {
            let coefficient = pattern[((cursor+1) / line) % pattern.len()];
            let mut num_to_process = cmp::min(line, input_signal_length - cursor);
            //println!("Index {} {} {}", cursor, num_to_process, ((cursor+1) / line) % pattern.len());
            if first_cycle {
                num_to_process = if line > 1 {line - 1} else {1};
                first_cycle = false;
            }
            let mut inner_cursor = cursor;
            let mut thesum = 0;
            if num_to_process > run_size {
                while inner_cursor < (cursor + num_to_process) {
                    let remain = num_to_process - (inner_cursor - cursor);
                    
                    if remain >= run_size_1000x {
                        thesum += runs1000x[inner_cursor];
                        inner_cursor += run_size_1000x;
                        run_hits += 1;
                    } else if remain >= run_size_100x {
                        thesum += runs100x[inner_cursor];
                        inner_cursor += run_size_100x;
                        run_hits += 1;
                    } else if remain >= run_size_10x {
                        thesum += runs10x[inner_cursor];
                        inner_cursor += run_size_10x;
                        run_hits += 1;
                    } else if remain >= run_size {
                        thesum += runs[inner_cursor];
                        inner_cursor += run_size;
                        run_hits += 1;
                    } else {
                        thesum += input_signal[inner_cursor..inner_cursor+remain].iter().sum::<u32>() as i32;
                        inner_cursor += remain;
                    }
                }
            } else {
                thesum = input_signal[cursor..cursor+num_to_process].iter().sum::<u32>() as i32;
            }
            if coefficient == 1 {
                total += thesum;
            } else if coefficient == -1 {
                total -= thesum;  
            }
            cursor += num_to_process;
        }
        totals[line - 1] = (i32::abs(total) % 10) as u32;
        if line % 100000 == 0 {
            println!("Totals {} time {:?} hits {}", line, start.elapsed(), run_hits );
            start = Instant::now();
        }
    }
    return totals;
}
