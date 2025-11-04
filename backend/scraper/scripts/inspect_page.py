import torch

if torch.cuda.is_available():
    print("✅ GPU disponible !")
    print("Nom du GPU :", torch.cuda.get_device_name(0))
else:
    print("⚠️ GPU non disponible, utilisation du CPU")