import multiprocessing
import platform
import json

try:
    import psutil
except ImportError:
    psutil = None


def detect_system():
    info = {
        "cpu_count_logical": multiprocessing.cpu_count(),
        "cpu_count_physical": None,
        "machine": platform.machine(),
        "processor": platform.processor(),
        "platform": platform.platform(),
        "total_ram_gb": None,
        "has_gpu": False,
        "gpu_name": None,
        "gpu_vram_gb": None,
    }

    if psutil is not None:
        try:
            info["cpu_count_physical"] = psutil.cpu_count(logical=False)
            vm = psutil.virtual_memory()
            info["total_ram_gb"] = round(vm.total / (1024**3), 2)
        except Exception:
            pass

    # Простейшая попытка детекта GPU без сторонних библиотек
    try:
        import subprocess

        # NVIDIA
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=1,
        )
        if result.returncode == 0 and result.stdout.strip():
            line = result.stdout.strip().splitlines()[0]
            name, vram = [x.strip() for x in line.split(",")]
            info["has_gpu"] = True
            info["gpu_name"] = name
            info["gpu_vram_gb"] = int(vram)
    except Exception:
        pass

    return info


def make_profiles(sysinfo):
    logical = sysinfo.get("cpu_count_logical") or 4
    physical = sysinfo.get("cpu_count_physical") or 2
    ram = sysinfo.get("total_ram_gb") or 8
    has_gpu = sysinfo.get("has_gpu", False)
    vram = sysinfo.get("gpu_vram_gb") or 0

    # THREADS
    threads_opt = max(2, min(physical, 8))
    threads_max = max(2, min(logical, 16))

    # CONTEXT_LENGTH
    if ram >= 32:
        ctx_opt = 4096
        ctx_max = 6144
    elif ram >= 16:
        ctx_opt = 3072
        ctx_max = 4096
    elif ram >= 8:
        ctx_opt = 3072
        ctx_max = 3072
    else:
        ctx_opt = 2048
        ctx_max = 3072

    # BATCH_SIZE
    if ram >= 32:
        batch_opt = 1024
        batch_max = 1536
    elif ram >= 16:
        batch_opt = 768
        batch_max = 1024
    elif ram >= 8:
        batch_opt = 512
        batch_max = 768
    else:
        batch_opt = 256
        batch_max = 384

    # GPU_LAYERS (если GPU нет — 0)
    if has_gpu and vram >= 8:
        gpu_layers_opt = 16
        gpu_layers_max = 24
    elif has_gpu and vram >= 4:
        gpu_layers_opt = 8
        gpu_layers_max = 12
    else:
        gpu_layers_opt = 0
        gpu_layers_max = 0

    profiles = {
        "optimal": {
            "MODEL_FILE": "tinyllama-tarot-q4_k_m.gguf",
            "MODEL_TYPE": "llama",
            "CONTEXT_LENGTH": ctx_opt,
            "THREADS": threads_opt,
            "GPU_LAYERS": gpu_layers_opt,
            "BATCH_SIZE": batch_opt,
        },
        "max_performance": {
            "MODEL_FILE": "tinyllama-tarot-q4_k_m.gguf",
            "MODEL_TYPE": "llama",
            "CONTEXT_LENGTH": ctx_max,
            "THREADS": threads_max,
            "GPU_LAYERS": gpu_layers_max,
            "BATCH_SIZE": batch_max,
        },
    }

    return profiles


def write_env_file(profile, filename="model.auto.env"):
    lines = [f"{k}={v}" for k, v in profile.items()]
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    sysinfo = detect_system()
    print("Detected system:")
    print(json.dumps(sysinfo, indent=2, ensure_ascii=False))

    profiles = make_profiles(sysinfo)
    print("\nGenerated profiles:")
    print(json.dumps(profiles, indent=2, ensure_ascii=False))

    # создаём файл с оптимальным профилем
    write_env_file(profiles["optimal"], filename="model.auto.env")
    print("\nmodel.auto.env created with optimal parameters")
