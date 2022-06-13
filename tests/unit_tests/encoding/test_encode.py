import pytest
from click.testing import CliRunner

from encoding import encode
from tests import data as test_data

fen_encoding = "r1bqk1nr/pp1n1ppp/4p3/2b5/4p3/2P1B3/PP1N1PPP/R2QKBNR w KQkq - 0 1"

native_encoding = (
    "Ra1 Qd1 Ke1 Bf1 Ng1 Rh1 Pa2 Pb2 Nd2 Pf2 Pg2 Ph2 Pc3 Be3 pe4 bc5 pe6 pa7 pb7 nd7 pf7 pg7 ph7 "
    "ra8 bc8 qd8 ke8 ng8 rh8\n"
)
activity_encoding = (
    "Bh6|0.67 Bg5|0.78 Bc5|0.78 Bf4|0.89 Bd4|0.89 Ne4|0.78 Nc4|0.78 Nf3|0.78 Nb3|0.78 Nb1|0.78 "
    "Nh3|0.78 Nf3|0.78 Ne2|0.78 Ba6|0.45 Bb5|0.56 Bc4|0.67 Bd3|0.78 Be2|0.89 Ke2|0.89 Qh5|0.56 "
    "Qg4|0.67 Qa4|0.67 Qf3|0.78 Qb3|0.78 Qe2|0.89 Qc2|0.89 Qc1|0.89 Qb1|0.78 Rc1|0.78 Rb1|0.89 "
    "Pc4|0.89 Ph3|0.89 Pg3|0.89 Pf3|0.89 Pb3|0.89 Pa3|0.89 Ph4|0.78 Pg4|0.78 Pf4|0.78 Pb4|0.78 "
    "Pa4|0.78 ne7|0.78 nh6|0.78 nf6|0.78 kf8|0.89 ke7|0.89 qe7|0.89 qc7|0.89 qf6|0.78 qb6|0.78 "
    "qg5|0.67 qa5|0.67 qh4|0.56 rb8|0.89 nf8|0.78 nb8|0.78 nf6|0.78 nb6|0.78 ne5|0.78 bf8|0.67 "
    "be7|0.78 bd6|0.89 bb6|0.89 bd4|0.89 bb4|0.89 be3|0.78 ba3|0.78 ph6|0.89 pg6|0.89 pf6|0.89 "
    "pb6|0.89 pa6|0.89 pe5|0.89 ph5|0.78 pg5|0.78 pf5|0.78 pb5|0.78 pa5|0.78\n"
)
connectivity_encoding = (
    "N>pe4 B>bc5 b>Be3 R<Qd1 R<Pa2 Q<Ra1 Q<Ke1 Q<Nd2 K<Qd1 K<Bf1 K<Nd2 K<Pf2 B<Pg2 R<Ng1 R<Ph2 "
    "P<Pc3 N<Bf1 P<Be3 B<Nd2 B<Pf2 b<pa7 n<bc5 p<pe6 r<pa7 r<bc8 b<pb7 b<nd7 q<nd7 q<bc8 q<ke8 "
    "k<nd7 k<pf7 k<qd8 r<ph7 r<ng8 R=pa7 R=ra8 Q=nd7 Q=qd8 R=ph7 R=rh8 N=pe4 B=bc5 B=pa7 b=Be3 "
    "b=Pf2 b=Ng1 r=Pa2 r=Ra1 q=Nd2 q=Qd1 r=Ph2 r=Rh1\n"
)
similarity_encoding = (
    f"{native_encoding[:-1]} {activity_encoding[:-1]} {connectivity_encoding[:-1]}\n"
)


@pytest.fixture(scope="module")
def cli_runner():
    yield CliRunner()


def test_naive(cli_runner):
    # WHEN
    result = cli_runner.invoke(encode.naive, ["--fen", fen_encoding])

    # THEN
    assert result.exit_code == 0
    assert result.output == native_encoding


def test_naive_input_file(cli_runner):
    # WHEN
    result = cli_runner.invoke(
        encode.naive, ["--input-file", f"{test_data.encoding_test_data_dir}/fen-encoding.txt"]
    )

    # THEN
    assert result.exit_code == 0
    assert result.output == native_encoding


def test_naive_output_file(cli_runner):
    # GIVEN
    naive_encoding_file = f"{test_data.tmp_dir}/naive-encoding.txt"

    # WHEN
    result = cli_runner.invoke(
        encode.naive, ["--fen", fen_encoding, "--output-file", naive_encoding_file]
    )

    # THEN
    assert result.exit_code == 0
    with open(naive_encoding_file) as output:
        assert output.read() == native_encoding


def test_activity(cli_runner):
    # WHEN
    result = cli_runner.invoke(encode.activity, ["--fen", fen_encoding])

    # THEN
    assert result.exit_code == 0
    assert result.output == activity_encoding


def test_activity_input_file(cli_runner):
    # WHEN
    result = cli_runner.invoke(
        encode.activity, ["--input-file", f"{test_data.encoding_test_data_dir}/fen-encoding.txt"]
    )

    # THEN
    assert result.exit_code == 0
    assert result.output == activity_encoding


def test_activity_output_file(cli_runner):
    # GIVEN
    activity_encoding_file = f"{test_data.tmp_dir}/activity-encoding.txt"

    # WHEN
    result = cli_runner.invoke(
        encode.activity, ["--fen", fen_encoding, "--output-file", activity_encoding_file]
    )

    # THEN
    assert result.exit_code == 0
    with open(activity_encoding_file) as output:
        assert output.read() == activity_encoding


def test_connectivity(cli_runner):
    # WHEN
    result = cli_runner.invoke(encode.connectivity, ["--fen", fen_encoding])

    # THEN
    assert result.exit_code == 0
    assert result.output == connectivity_encoding


def test_connectivity_input_file(cli_runner):
    # WHEN
    result = cli_runner.invoke(
        encode.connectivity,
        ["--input-file", f"{test_data.encoding_test_data_dir}/fen-encoding.txt"],
    )

    # THEN
    assert result.exit_code == 0
    assert result.output == connectivity_encoding


def test_connectivity_output_file(cli_runner):
    # GIVEN
    connectivity_encoding_file = f"{test_data.tmp_dir}/connectivity-encoding.txt"

    # WHEN
    result = cli_runner.invoke(
        encode.connectivity, ["--fen", fen_encoding, "--output-file", connectivity_encoding_file]
    )

    # THEN
    assert result.exit_code == 0
    with open(connectivity_encoding_file) as output:
        assert output.read() == connectivity_encoding


def test_similarity(cli_runner):
    # WHEN
    result = cli_runner.invoke(encode.similarity, ["--fen", fen_encoding])

    # THEN
    assert result.exit_code == 0
    assert result.output == similarity_encoding


def test_similarity_input_file(cli_runner):
    # WHEN
    result = cli_runner.invoke(
        encode.similarity, ["--input-file", f"{test_data.encoding_test_data_dir}/fen-encoding.txt"]
    )

    # THEN
    assert result.exit_code == 0
    assert result.output == similarity_encoding


def test_similarity_output_file(cli_runner):
    # GIVEN
    similarity_encoding_file = f"{test_data.tmp_dir}/similarity-encoding.txt"

    # WHEN
    result = cli_runner.invoke(
        encode.similarity, ["--fen", fen_encoding, "--output-file", similarity_encoding_file]
    )

    # THEN
    assert result.exit_code == 0
    with open(similarity_encoding_file) as output:
        assert output.read() == similarity_encoding
