import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

st.set_page_config(
    page_title="Cálculo Lab | Método de la arandela",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background: #0b1120; color: #eef2ff; }
.block-container { padding-top: 2rem; max-width: 1250px; }
h1, h2, h3, p, label { color: #eef2ff !important; }
div[data-testid="stMetric"] {
    background: #121d33; border: 1px solid #263652;
    padding: 16px; border-radius: 14px;
}
div.stButton > button { border-radius: 10px; min-height: 2.8rem; font-weight: 600; }
.help { color: #aab6cc; }
</style>
""", unsafe_allow_html=True)

x = sp.symbols("x", real=True)

def parse_function(expr):
    expr = expr.strip().replace("^", "**")
    if not expr:
        raise ValueError("Debes escribir una función.")
    parsed = sp.sympify(
        expr,
        locals={
            "x": x, "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos,
            "tan": sp.tan, "exp": sp.exp, "log": sp.log, "ln": sp.log,
            "pi": sp.pi, "abs": sp.Abs
        }
    )
    if parsed.free_symbols - {x}:
        raise ValueError("Usa solamente la variable x.")
    return parsed

def fmt_expr(expr):
    """Formato matemático legible para mostrar expresiones."""
    return sp.latex(sp.simplify(expr))

def simpson_integral(func, lower, upper, intervals):
    if intervals % 2 != 0:
        raise ValueError("El número de subintervalos debe ser par para Simpson 1/3.")
    xs = np.linspace(lower, upper, int(intervals) + 1)
    ys = np.asarray(func(xs), dtype=float)
    if ys.ndim == 0:
        ys = np.full_like(xs, float(ys), dtype=float)
    if not np.all(np.isfinite(ys)):
        raise ValueError("La función tiene valores no definidos en el intervalo.")
    h = (upper - lower) / intervals
    result = h / 3 * (ys[0] + ys[-1] + 4 * np.sum(ys[1:-1:2]) + 2 * np.sum(ys[2:-1:2]))
    return result, xs, ys

def mostrar_procedimiento(R, r, a, b, integral_num, volumen_num):
    st.markdown("### Paso 1. Escribir la fórmula del método de la arandela")
    st.latex(r"V=\pi\int_a^b\left[R(x)^2-r(x)^2\right]\,dx")

    st.markdown("### Paso 2. Sustituir las funciones y los límites")
    st.latex(
        rf"V=\pi\int_{{{sp.latex(sp.sympify(a))}}}^{{{sp.latex(sp.sympify(b))}}}"
        rf"\left[({sp.latex(R)})^2-({sp.latex(r)})^2\right]\,dx"
    )

    R2 = sp.expand(R**2)
    r2 = sp.expand(r**2)
    st.markdown("### Paso 3. Desarrollar los cuadrados")
    st.write("Elevamos al cuadrado el radio exterior:")
    st.latex(rf"R(x)^2=({sp.latex(R)})^2={sp.latex(R2)}")
    st.write("Elevamos al cuadrado el radio interior:")
    st.latex(rf"r(x)^2=({sp.latex(r)})^2={sp.latex(r2)}")

    integrando_expandido = sp.expand(R2 - r2)
    integrando_simplificado = sp.simplify(integrando_expandido)
    st.markdown("### Paso 4. Restar y simplificar")
    st.latex(
        rf"R(x)^2-r(x)^2={sp.latex(R2)}-({sp.latex(r2)})"
    )
    st.latex(rf"={sp.latex(integrando_simplificado)}")
    st.write("La integral queda:")
    st.latex(
        rf"V=\pi\int_{{{sp.latex(sp.sympify(a))}}}^{{{sp.latex(sp.sympify(b))}}}"
        rf"\left({sp.latex(integrando_simplificado)}\right)\,dx"
    )

    st.markdown("### Paso 5. Integrar término por término")
    antiderivada = sp.integrate(integrando_simplificado, x)
    st.write("Integramos la expresión simplificada con respecto a x:")
    st.latex(rf"\int \left({sp.latex(integrando_simplificado)}\right)dx"
             rf"={sp.latex(antiderivada)}+C")
    st.write("Por tanto, aplicando los límites:")
    st.latex(
        rf"V=\pi\left[{sp.latex(antiderivada)}\right]_"
        rf"{{{sp.latex(sp.sympify(a))}}}^{{{sp.latex(sp.sympify(b))}}}"
    )

    st.markdown("### Paso 6. Sustituir los límites de integración")
    ant_b = sp.simplify(antiderivada.subs(x, sp.sympify(b)))
    ant_a = sp.simplify(antiderivada.subs(x, sp.sympify(a)))
    st.write(f"Sustituimos el límite superior x = {b}:")
    st.latex(rf"F({sp.latex(sp.sympify(b))})={sp.latex(ant_b)}")
    st.write(f"Sustituimos el límite inferior x = {a}:")
    st.latex(rf"F({sp.latex(sp.sympify(a))})={sp.latex(ant_a)}")
    integral_exacta = sp.simplify(ant_b - ant_a)
    st.write("Restamos el valor inferior al valor superior:")
    st.latex(
        rf"\int_a^b\left[R(x)^2-r(x)^2\right]dx"
        rf"={sp.latex(ant_b)}-({sp.latex(ant_a)})"
        rf"={sp.latex(integral_exacta)}"
    )

    st.markdown("### Paso 7. Calcular el volumen")
    volumen_exacto = sp.simplify(sp.pi * integral_exacta)
    st.write("Multiplicamos la integral por π:")
    st.latex(rf"V=\pi\left({sp.latex(integral_exacta)}\right)"
             rf"={sp.latex(volumen_exacto)}")
    st.write("Resultado decimal:")
    st.latex(rf"V\approx {volumen_num:.8f}\ \text{{unidades cúbicas}}")
    st.caption(
        f"El valor numérico se calculó con la regla compuesta de Simpson 1/3 "
        f"y se aproxima a {volumen_num:.8f}. La expresión exacta anterior "
        f"se obtiene simbólicamente para estas funciones."
    )

st.title("CALCULO LAB")
st.subheader("Proyecto de Cálculo II · Método de la arandela")
st.markdown("---")
st.header("Cálculo del volumen")
st.write("Ingresa los radios y los límites de integración. El programa aproximará el volumen mediante Simpson 1/3 y mostrará el procedimiento matemático paso a paso.")

with st.expander("Fórmula y explicación", expanded=False):
    st.latex(r"V=\pi\int_a^b\left[R(x)^2-r(x)^2\right]\,dx")
    st.write("R(x) es el radio exterior, r(x) el radio interior y [a,b] el intervalo de integración. Los radios deben ser no negativos y R(x) debe ser mayor o igual que r(x) en el intervalo.")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("### Funciones")
    R_text = st.text_input("Radio exterior R(x)", value="x**3+2", placeholder="Ejemplo: x**2")
    r_text = st.text_input("Radio interior r(x)", value="x**2", placeholder="Ejemplo: x")
with col2:
    st.markdown("### Límites de integración")
    a = st.number_input("Límite inferior a", value=0.0, step=0.5, format="%.4f")
    b = st.number_input("Límite superior b", value=2.0, step=0.5, format="%.4f")
    n = st.number_input("Número de subintervalos (debe ser par)", min_value=2, max_value=200000, value=1000, step=2)

button_col1, button_col2, button_col3 = st.columns([2, 1, 1])
with button_col1:
    calculate = st.button("Calcular volumen", type="primary", use_container_width=True)
with button_col2:
    example = st.button("Cargar ejemplo", use_container_width=True)
with button_col3:
    clear = st.button("Limpiar datos", use_container_width=True)

if example:
    st.info("Ejemplo sugerido: R(x)=x**3+2, r(x)=x**2, intervalo [0, 2]. Si los campos no se actualizan automáticamente, escríbelos manualmente.")
if clear:
    st.info("Para limpiar los campos, borra las funciones y vuelve a introducir los datos deseados.")

if calculate:
    try:
        if b <= a:
            raise ValueError("El límite superior b debe ser mayor que el límite inferior a.")
        if int(n) % 2:
            raise ValueError("El número de subintervalos debe ser par. Por ejemplo: 1000.")

        R_expr = parse_function(R_text)
        r_expr = parse_function(r_text)
        R_func = sp.lambdify(x, R_expr, modules=["numpy"])
        r_func = sp.lambdify(x, r_expr, modules=["numpy"])

        xs_check = np.linspace(a, b, 2001)
        R_check = np.asarray(R_func(xs_check), dtype=float)
        r_check = np.asarray(r_func(xs_check), dtype=float)
        if R_check.ndim == 0:
            R_check = np.full_like(xs_check, float(R_check))
        if r_check.ndim == 0:
            r_check = np.full_like(xs_check, float(r_check))
        if not np.all(np.isfinite(R_check)) or not np.all(np.isfinite(r_check)):
            raise ValueError("Alguna función no está definida en todo el intervalo.")
        if np.any(R_check < -1e-9) or np.any(r_check < -1e-9):
            raise ValueError("Los radios no pueden ser negativos en el intervalo.")
        if np.any(R_check + 1e-8 < r_check):
            raise ValueError("El radio exterior R(x) debe ser mayor o igual que el radio interior r(x) en todo el intervalo.")

        def integrand(z):
            return np.asarray(R_func(z), dtype=float)**2 - np.asarray(r_func(z), dtype=float)**2

        integral_num, xs, integrand_values = simpson_integral(integrand, a, b, int(n))
        volume_num = math.pi * integral_num
        if volume_num < -1e-7:
            raise ValueError("El volumen calculado resultó negativo; revisa los radios y límites.")
        volume_num = max(0.0, volume_num)

        st.markdown("---")
        st.header("Resultado")
        m1, m2, m3 = st.columns(3)
        m1.metric("Volumen aproximado", f"{volume_num:.6f} u³")
        m2.metric("Integral sin π", f"{integral_num:.6f}")
        m3.metric("Subintervalos", f"{int(n):,}")
        st.success(f"El volumen aproximado por el método de la arandela es **{volume_num:.6f} unidades cúbicas**.")

        with st.expander("Ver procedimiento completo paso a paso", expanded=True):
            mostrar_procedimiento(R_expr, r_expr, a, b, integral_num, volume_num)

        xplot = np.linspace(a, b, 500)
        Rp = np.asarray(R_func(xplot), dtype=float)
        rp = np.asarray(r_func(xplot), dtype=float)
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Radios exterior e interior", "Integrando R(x)² − r(x)²"))
        fig.add_trace(go.Scatter(x=xplot, y=Rp, mode="lines", name="R(x)", line=dict(width=3)), row=1, col=1)
        fig.add_trace(go.Scatter(x=xplot, y=rp, mode="lines", name="r(x)", line=dict(width=3)), row=1, col=1)
        fig.add_trace(go.Scatter(x=xplot, y=Rp**2-rp**2, mode="lines", fill="tozeroy", name="R² − r²", line=dict(width=3)), row=1, col=2)
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1120", plot_bgcolor="#111b2e",
                          font=dict(color="#eef2ff"), height=450, margin=dict(l=20,r=20,t=60,b=20),
                          legend=dict(orientation="h", y=-0.2))
        fig.update_xaxes(title_text="x", gridcolor="#263652")
        fig.update_yaxes(title_text="Radio", gridcolor="#263652", row=1, col=1)
        fig.update_yaxes(title_text="R(x)² − r(x)²", gridcolor="#263652", row=1, col=2)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"No se pudo calcular el volumen: {e}")
        st.info("Prueba: R(x)=x**3+2, r(x)=x**2, a=0, b=2, subintervalos=1000.")

st.markdown("---")
st.caption("Cálculo Lab · Método numérico de la arandela · Regla compuesta de Simpson 1/3")
