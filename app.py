import streamlit as st
import pydeck as pdk
import polyline


# get query parameters
# ?polygon=
query_parameters = st.experimental_get_query_params()


def decode_polyline(poly_str):
    """Decodes a Google Maps encoding polyline string."""
    decoded = polyline.decode(poly_str)
    # Flip the latitudes and longitudes for Pydeck
    return [(lon, lat) for lat, lon in decoded]

# Streamlit UI
st.title("Polyline Decoder")

input_polyline = st.text_input("Enter the encoded polyline:", value = query_parameters["polyline"][0] if "polyline" in query_parameters else "")

if input_polyline:
    decoded_path = decode_polyline(input_polyline)

    if decoded_path:
        if len(decoded_path) == 1:  # Handle single point
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=[{"position": decoded_path[0], "color": [255, 0, 0], "radius": 100}],
                get_position="position",
                get_color="color",
                get_radius="radius",
            )
        else:
            layer = pdk.Layer(
                "PathLayer",
                data=[
                    {
                        "path": decoded_path,
                        "color": [255, 0, 0],
                    }
                ],
                get_path="path",
                get_color="color",
                width_min_pixels=5,
            )

        view_state = pdk.ViewState(
            longitude=decoded_path[0][0], latitude=decoded_path[0][1], zoom=10
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    else:
        st.write("Failed to decode the polyline.")
else:
    st.write("Enter a polyline to see it on the map.")

with st.expander("Query parameter"):
    st.write("Query parameter could be added through adding ?polyline=[POLYLINE CODE HERE]")
