import time

import numpy as np
from pycuda.driver import init, register_host_memory, Device, aligned_zeros
from pycuda.gpuarray import GPUArray


NUM_ITERATIONS = 10
SIZE = 100_000_000


def main():
    init()
    d = Device(0)
    ctx = d.make_context()

    t0 = time.monotonic_ns()
    a = aligned_zeros((1, SIZE), dtype=np.int64)
    t1 = time.monotonic_ns()
    a = register_host_memory(a)
    t2 = time.monotonic_ns()
    gpu_a = GPUArray(a.shape, a.dtype)
    t3 = time.monotonic_ns()
    for _ in range(NUM_ITERATIONS):
        gpu_a.set(a)
        gpu_a += 1
        gpu_a.get(a)
    t4 = time.monotonic_ns()

    ctx.pop()

    print(a)
    print(f"allocate CPU memory {t1 - t0:,}")
    print(f"register CPU memory {t2 - t1:,}")
    print(f"allocate GPU memory {t3 - t2:,}")
    print(f"compute {t4 - t3:,}")


if __name__ == "__main__":
    main()
