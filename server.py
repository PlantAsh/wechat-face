from waitress import serve
import connect as con

serve(con.app, port=80)
