import math, time, sys
from quantum_core import Qubit, QuantumTeleportProtocol, AdvancedMatterTeleporter
from matter_teleporter import MatterScanner, QuantumTeleporter

def test_qubit_teleport():
    print("--- تست کیوبیت ---")
    proto = QuantumTeleportProtocol()
    psi = Qubit(complex(1/math.sqrt(2)), complex(1/math.sqrt(2)))
    psi_initial = (psi.alpha, psi.beta)
    start = time.perf_counter()
    psi_out = proto.teleport(psi)
    elapsed = (time.perf_counter() - start) * 1000
    fidelity = abs(psi_initial[0].conjugate()*psi_out.alpha + psi_initial[1].conjugate()*psi_out.beta)**2
    print(f"زمان: {elapsed:.3f} ms | وفاداری: {fidelity:.4f}")
    return fidelity > 0.99, elapsed

def test_matter_adv():
    print("--- تست ماده پیشرفته ---")
    adv = AdvancedMatterTeleporter()
    start = time.perf_counter()
    energy, msg = adv.teleport_element(26)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"زمان: {elapsed:.3f} ms | انرژی: {energy:.2e} J")
    return energy > 0, elapsed

def test_molecule():
    print("--- تست مولکول ---")
    qt = QuantumTeleporter()
    start = time.perf_counter()
    report = qt.teleport_molecule("H2O")
    elapsed = (time.perf_counter() - start) * 1000
    print(f"زمان: {elapsed:.3f} ms")
    return "✅" in report, elapsed

def main():
    results = []
    try:
        r,t = test_qubit_teleport(); results.append(("کیوبیت", r, t))
    except Exception as e:
        results.append(("کیوبیت", False, str(e)))
    try:
        r,t = test_matter_adv(); results.append(("ماده", r, t))
    except Exception as e:
        results.append(("ماده", False, str(e)))
    try:
        r,t = test_molecule(); results.append(("مولکول", r, t))
    except Exception as e:
        results.append(("مولکول", False, str(e)))

    print("\n===== گزارش نهایی =====")
    all_ok = True
    for name, status, val in results:
        s = "✅" if status else "❌"
        v = f"{val:.3f} ms" if isinstance(val, (int,float)) else str(val)
        print(f"{s} {name}: {v}")
        if not status:
            all_ok = False

    if all_ok:
        print("🎯 تمام تست‌ها با موفقیت گذشت.")
    else:
        print("⚠️ شکست در برخی تست‌ها. بررسی کنید.")
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
