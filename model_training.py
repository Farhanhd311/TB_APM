

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import joblib
import warnings

from sklearn.ensemble         import RandomForestRegressor
from sklearn.model_selection  import train_test_split
from sklearn.metrics          import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 0. BUAT FOLDER OUTPUT
# ─────────────────────────────────────────────
os.makedirs('model',           exist_ok=True)
os.makedirs('hasil_evaluasi',  exist_ok=True)


# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
print("=" * 55)
print("  TAHAP 1 — LOAD DATA")
print("=" * 55)

df = pd.read_csv('exercise.csv')
print(f"  Jumlah baris   : {len(df):,}")
print(f"  Jumlah kolom   : {df.shape[1]}")
print(f"  Missing values : {df.isnull().sum().sum()}")
print(f"  Duplikat       : {df.duplicated().sum()}")


# ─────────────────────────────────────────────
# 2. PREPROCESSING
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  TAHAP 2 — PREPROCESSING")
print("=" * 55)

# Hapus kolom User_ID (tidak relevan untuk prediksi)
df = df.drop(columns=['User_ID'])
print("  ✓ Kolom User_ID dihapus")

# Encoding Gender: male → 1, female → 0
df['Gender'] = df['Gender'].map({'male': 1, 'female': 0})
print("  ✓ Encoding Gender: male=1, female=0")

# Pisahkan fitur (X) dan target (y)
X = df.drop(columns=['Calories'])
y = df['Calories']

FITUR = list(X.columns)
print(f"  ✓ Fitur yang digunakan: {FITUR}")
print(f"  ✓ Target              : Calories")

# Split data 80% train — 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n  Data training : {X_train.shape[0]:,} baris ({int(X_train.shape[0]/len(df)*100)}%)")
print(f"  Data testing  : {X_test.shape[0]:,} baris ({int(X_test.shape[0]/len(df)*100)}%)")


# ─────────────────────────────────────────────
# 3. TRAINING MODEL
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  TAHAP 3 — TRAINING MODEL RANDOM FOREST")
print("=" * 55)

# Parameter model
PARAMS = {
    'n_estimators' : 100,   # jumlah pohon keputusan
    'max_depth'    : None,  # kedalaman pohon (None = tidak dibatasi)
    'min_samples_split': 2, # minimum sampel untuk split node
    'min_samples_leaf' : 1, # minimum sampel di daun pohon
    'random_state' : 42,    # agar hasil reproducible
    'n_jobs'       : -1,    # pakai semua core CPU
}

print(f"  Parameter model:")
for k, v in PARAMS.items():
    print(f"    {k:<22}: {v}")

model = RandomForestRegressor(**PARAMS)

print("\n  Melatih model... ", end='', flush=True)
model.fit(X_train, y_train)
print("selesai ✓")

# Simpan model ke file .pkl
MODEL_PATH = 'model/random_forest_model.pkl'
joblib.dump(model, MODEL_PATH)
print(f"\n  ✓ Model disimpan ke: {MODEL_PATH}")


# ─────────────────────────────────────────────
# 4. EVALUASI MODEL
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  TAHAP 4 — EVALUASI MODEL")
print("=" * 55)

y_pred       = model.predict(X_test)
y_pred_train = model.predict(X_train)

mae   = mean_absolute_error(y_test,  y_pred)
rmse  = np.sqrt(mean_squared_error(y_test, y_pred))
r2    = r2_score(y_test,  y_pred)
r2_tr = r2_score(y_train, y_pred_train)

print(f"\n  {'Metrik':<30} {'Nilai':>10}")
print(f"  {'-'*42}")
print(f"  {'MAE  (Mean Absolute Error)':<30} {mae:>10.4f}")
print(f"  {'RMSE (Root Mean Sq. Error)':<30} {rmse:>10.4f}")
print(f"  {'R²   (Test)':<30} {r2:>10.4f}")
print(f"  {'R²   (Train)':<30} {r2_tr:>10.4f}")
print(f"\n  Interpretasi:")
print(f"  → MAE {mae:.2f} artinya rata-rata prediksi meleset ±{mae:.1f} kkal")
print(f"  → R² {r2:.4f} artinya model menjelaskan {r2*100:.2f}% variansi data")

# Feature Importance
fi = pd.Series(model.feature_importances_, index=FITUR).sort_values(ascending=False)
print(f"\n  Feature Importance:")
for feat, val in fi.items():
    bar = '█' * int(val * 40)
    print(f"    {feat:<12} {val:.4f}  {bar}")


# ─────────────────────────────────────────────
# 5. VISUALISASI EVALUASI
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  TAHAP 5 — MEMBUAT GRAFIK EVALUASI")
print("=" * 55)

fig = plt.figure(figsize=(18, 12))
fig.suptitle('Evaluasi Model Random Forest — Prediksi Kalori',
             fontsize=16, fontweight='bold', y=1.01)
fig.patch.set_facecolor('#F8F9FA')

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.40, wspace=0.35)

BLUE   = '#4A90D9'
GREEN  = '#27AE60'
ORANGE = '#E67E22'
RED    = '#E74C3C'

# ── Plot 1: Aktual vs Prediksi ────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
ax1.scatter(y_test, y_pred, alpha=0.25, s=10, color=BLUE, label='Prediksi')
lims = [0, max(y_test.max(), y_pred.max()) + 10]
ax1.plot(lims, lims, 'r--', linewidth=1.5, label='Prediksi sempurna')
ax1.set_xlabel('Kalori Aktual (kcal)', fontsize=11)
ax1.set_ylabel('Kalori Prediksi (kcal)', fontsize=11)
ax1.set_title(f'Aktual vs Prediksi  |  R² = {r2:.4f}', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.set_facecolor('#FFFFFF')
ax1.grid(alpha=0.3)

# ── Plot 2: Feature Importance ───────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
colors_fi = [BLUE if i == 0 else '#85B7EB' for i in range(len(fi))]
bars = ax2.barh(fi.index[::-1], fi.values[::-1], color=colors_fi[::-1],
                edgecolor='white', height=0.6)
ax2.set_title('Feature Importance', fontsize=12, fontweight='bold')
ax2.set_xlabel('Tingkat Kepentingan')
ax2.set_facecolor('#FFFFFF')
ax2.grid(axis='x', alpha=0.3)
for bar, val in zip(bars, fi.values[::-1]):
    ax2.text(val + 0.005, bar.get_y() + bar.get_height()/2,
             f'{val:.3f}', va='center', fontsize=9)

# ── Plot 3: Distribusi Residual ──────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
residuals = y_test.values - y_pred
ax3.hist(residuals, bins=50, color=GREEN, edgecolor='white', alpha=0.85)
ax3.axvline(0, color='red', linestyle='--', linewidth=1.5)
ax3.set_xlabel('Residual (Aktual − Prediksi)', fontsize=11)
ax3.set_ylabel('Frekuensi', fontsize=11)
ax3.set_title('Distribusi Residual', fontsize=12, fontweight='bold')
ax3.set_facecolor('#FFFFFF')
ax3.grid(alpha=0.3)

# ── Plot 4: Residual vs Prediksi ────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.scatter(y_pred, residuals, alpha=0.2, s=10, color=ORANGE)
ax4.axhline(0, color='red', linestyle='--', linewidth=1.5)
ax4.set_xlabel('Kalori Prediksi (kcal)', fontsize=11)
ax4.set_ylabel('Residual', fontsize=11)
ax4.set_title('Residual vs Prediksi', fontsize=12, fontweight='bold')
ax4.set_facecolor('#FFFFFF')
ax4.grid(alpha=0.3)

# ── Plot 5: Metrik Ringkasan ─────────────────────────────
ax5 = fig.add_subplot(gs[1, 2])
ax5.axis('off')
metrik_data = [
    ['MAE',         f'{mae:.4f}',   'kcal'],
    ['RMSE',        f'{rmse:.4f}',  'kcal'],
    ['R² (Test)',   f'{r2:.4f}',    ''],
    ['R² (Train)',  f'{r2_tr:.4f}', ''],
    ['Data Train',  f'{X_train.shape[0]:,}', 'baris'],
    ['Data Test',   f'{X_test.shape[0]:,}',  'baris'],
]
tbl = ax5.table(
    cellText=metrik_data,
    colLabels=['Metrik', 'Nilai', 'Satuan'],
    loc='center', cellLoc='center'
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.8)
for (r, c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor('#4A90D9')
        cell.set_text_props(color='white', fontweight='bold')
    else:
        cell.set_facecolor('#F0F4FA' if r % 2 == 0 else '#FFFFFF')
    cell.set_edgecolor('#DDDDDD')
ax5.set_title('Ringkasan Metrik', fontsize=12, fontweight='bold', pad=80)

GRAFIK_PATH = 'hasil_evaluasi/evaluasi_model.png'
plt.savefig(GRAFIK_PATH, dpi=130, bbox_inches='tight')
plt.close()
print(f"  ✓ Grafik disimpan ke: {GRAFIK_PATH}")


# ─────────────────────────────────────────────
# 6. CONTOH PREDIKSI
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  TAHAP 6 — CONTOH PREDIKSI MANUAL")
print("=" * 55)

# Format: Gender(1=male,0=female), Age, Height, Weight, Duration, Heart_Rate, Body_Temp
contoh_data = pd.DataFrame({
    'Gender'    : [1,      0      ],
    'Age'       : [25,     30     ],
    'Height'    : [175,    162    ],
    'Weight'    : [70,     55     ],
    'Duration'  : [30,     45     ],
    'Heart_Rate': [110,    125    ],
    'Body_Temp' : [40.5,   40.8   ],
})

hasil_prediksi = model.predict(contoh_data)

print(f"\n  {'No':<4} {'Gender':<8} {'Usia':<6} {'Durasi':<8} {'Heart':<7} {'Prediksi':>10}")
print(f"  {'-'*48}")
gender_label = {1: 'Male', 0: 'Female'}
for i, (_, row) in enumerate(contoh_data.iterrows()):
    g = gender_label[int(row['Gender'])]
    print(f"  {i+1:<4} {g:<8} {int(row['Age']):<6} {int(row['Duration']):<8} "
          f"{int(row['Heart_Rate']):<7} {hasil_prediksi[i]:>8.1f} kcal")

print("\n" + "=" * 55)
print("  SELESAI! File output:")
print(f"  → {MODEL_PATH}")
print(f"  → {GRAFIK_PATH}")
print("=" * 55)
