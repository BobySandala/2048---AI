# test_queue.py
from multiprocessing import Process, Queue
import time
import src.globals as globals

# Writer process: simulates GA training
def writer(steps=10):
    for step in range(steps):
        progress = (step + 1) / steps
        globals.queue.put({"progress": progress})
        time.sleep(0.2)  # simulate work
    globals.queue.put("DONE")  # signal that training is finished

# Main process: reads updates from the queue
def main():
    
    p = Process(target=writer, args=())
    p.start()
    
    train_progress = {"progress": 0.0}
    running = True
    
    while running:
        # Poll queue for new updates
        while not globals.queue.empty():
            msg = globals.queue.get()
            if msg == "DONE":
                running = False
            else:
                train_progress = msg
        
        # Display the latest progress
        print(f"Progress: {train_progress['progress']*100:.2f}%")
        time.sleep(0.1)  # simulate frame delay / main loop

    p.join()
    print("Training finished!")

if __name__ == "__main__":
    main()
