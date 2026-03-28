import streamlit as st
import numpy as np

st.title("Y-Bus Matrix Calculator")

# Step 1: Number of buses and lines
n = st.number_input("Enter number of buses", min_value=1, step=1, value=3)
lines = st.number_input("Enter number of transmission lines", min_value=1, step=1, value=3)

# Step 2: Impedance or Admittance
choice = st.radio("Select line value input type", ("Impedance (converted to admittance)", "Admittance (used directly)"))
use_impedance = choice.startswith("Impedance")

# Step 3: Line data
line_data = []
st.subheader("Enter line data")
for k in range(int(lines)):
    st.markdown(f"**Line {k+1}**")
    from_bus = st.number_input(f"From bus (Line {k+1})", min_value=1, max_value=int(n), step=1, key=f"from{k}")
    to_bus = st.number_input(f"To bus (Line {k+1})", min_value=1, max_value=int(n), step=1, key=f"to{k}")
    val_input = st.text_input(f"Enter value (complex, e.g., 0.02+0.04j) for Line {k+1}", key=f"val{k}")
    line_data.append((from_bus-1, to_bus-1, val_input))

# Step 4: Line charging per bus
st.subheader("Enter line charging admittance per bus")
Yc_bus = []
for i in range(int(n)):
    s = st.text_input(f"Bus {i+1} line charging admittance (0 if none, e.g., 0.0001j)", key=f"yc{i}")
    Yc_bus.append(s)

# Step 5: Calculate Y-bus on button click
if st.button("Calculate Y-bus"):
    Y = np.zeros((int(n), int(n)), dtype=complex)
    # Add lines
    for from_bus, to_bus, val_input in line_data:
        try:
            val = complex(val_input.replace(" ",""))
            Y_line = 1/val if use_impedance else val
            Y[from_bus][to_bus] -= Y_line
            Y[to_bus][from_bus] -= Y_line
            Y[from_bus][from_bus] += Y_line
            Y[to_bus][to_bus] += Y_line
        except:
            st.error(f"Invalid line value: {val_input}")
            st.stop()
    # Add line charging
    for i, s in enumerate(Yc_bus):
        try:
            Yc = complex(s.replace(" ",""))
            Y[i,i] += Yc
        except:
            st.error(f"Invalid line charging value: {s}")
            st.stop()
    # Display Y-bus
    st.subheader("Y-bus Matrix")
    st.write(Y)