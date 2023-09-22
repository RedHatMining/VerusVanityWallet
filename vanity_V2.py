from bitcoin import *
import argparse
import threading
from time import perf_counter

novalids = [' ']

def load_prefixes_from_file(file_path):
    with open(file_path, "r") as f:
        prefixes = [line.strip() for line in f.readlines()]
    return prefixes

def vanity_btc(prefixes, filen="", mode="prefix", case_sensitive=False, nthreads=4):

    for a in novalids:
        if any(a in prefix for prefix in prefixes):
            print('Invalid characters found in prefixes. Program will exit.')
            exit()

    if not prefixes:
        print('Error: No prefixes loaded from file. Program will now exit.')
        exit()

    def generate_and_check(tc):
        encontrada = False
        current_thread = threading.current_thread()
        thread_name = current_thread.name
        print(f"Thread {thread_name} is running.")
        while not encontrada:
            priv = random_key()
            pub = privkey_to_pubkey(priv)
            pub = compress(pub)
            addr = pubkey_to_address(pub, 0x3c)
            if not case_sensitive:
                addr_lower = addr.lower()
                for prefix in prefixes:
                    prefix_lower = prefix.lower()
                    if mode == "prefix" and addr_lower.startswith(prefix_lower):
                        sp = prefix
                        encontrada = True
                    elif mode == "suffix" and addr_lower.endswith(prefix_lower):
                        sp = prefix
                        encontrada = True
                    elif mode == "substring" and prefix_lower in addr_lower:
                        sp = prefix
                        encontrada = True
            else:
                for prefix in prefixes:
                    if mode == "prefix" and addr.startswith(prefix):
                        sp = prefix
                        encontrada = True
                    elif mode == "suffix" and addr.endswith(prefix):
                        sp = prefix
                        encontrada = True
                    elif mode == "substring" and prefix in addr:
                        sp = prefix
                        encontrada = True
                    if encontrada:
                        pass

            if encontrada:
                with open(filen, "a") as f:
                    f.write(f'##############################{sp}##############################\n')
                    f.write(f"private key: {priv}\n")
                    f.write(f"public key: {pub}\n")
                    f.write(f"Address: {addr}\n")
                    found(addr, pub, priv, tc)
                    encontrada = False
            counts[tc - 1] += 1

    def found(addr, pub, priv, tc):
        print("#" * 210)
        print(f"T{tc} found: \033[5m\033[38;2;0;255;0m{addr}\033[0m")
        print(f"T1W/s {counts[0] / (perf_counter() - start_time)}\nT2W/s {counts[1] / (perf_counter() - start_time)}\nT3W/s {counts[2] / (perf_counter() - start_time)}\nT4W/s {counts[3] / (perf_counter() - start_time)}\nT5W/s {counts[4] / (perf_counter() - start_time)}\nT6W/s {counts[5] / (perf_counter() - start_time)}\nT7W/s {counts[6] / (perf_counter() - start_time)}\nT8W/s {counts[7] / (perf_counter() - start_time)}\nT9W/s {counts[8] / (perf_counter() - start_time)}\nT10W/s {counts[9] / (perf_counter() - start_time)}\nT11W/s {counts[10] / (perf_counter() - start_time)}\nT12W/s {counts[11] / (perf_counter() - start_time)}")
        print(f"Total Wallets Per Second: {(counts[0] + counts[1] + counts[2] + counts[3] + counts[4] + counts[5] + counts[6] + counts[7] + counts[8] + counts[9] + counts[10] + counts[11]) / (perf_counter() - start_time)}")

    encontrada = False
    start_time = perf_counter()
    counts = [0] * nthreads
    num_threads = nthreads

    threads = []
    for i in range(1, num_threads + 1):
        thread = threading.Thread(target=generate_and_check, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    parser = argparse.ArgumentParser(description='Vanity Bitcoin address generator')
    parser.add_argument('prefix_file', type=str, help='Path to the file containing prefixes')
    parser.add_argument('-of', '--output_file', type=str, default='', help='Name and extension of the file to save the results')
    parser.add_argument('--case_sensitive', action='store_true', help='Case sensitive search')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Number of threads to use')
    parser.add_argument('-f', '--format', type=str, default='prefix', help='The format of the vanity prefix, suffix, or substring')
    args = parser.parse_args()
    prefixes = load_prefixes_from_file(args.prefix_file)
    if not args.output_file:
        args.output_file = 'vanity_results.txt'
    
    banner = f"""
#################################################################################################################################################################################################################
                                                                                                 WALLET MINER                                                                      
Loaded Prefixes {len(load_prefixes_from_file(args.prefix_file))}
Format {args.format}
Threads {args.threads}
Made By: Mrhakdev
#################################################################################################################################################################################################################"""
    print(banner)
    vanity_btc(prefixes, args.output_file, mode=args.format, case_sensitive=args.case_sensitive, nthreads=args.threads)
if __name__ == '__main__':
    main()