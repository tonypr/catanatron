from catanatron.game import Game
from catanatron.models.enums import Action, ActionType
from catanatron.models.player import Color
from catanatron.models.board import longest_acyclic_path


def build_initial_placements(
    game: Game,
    p0_actions=[0, (0, 1), 2, (1, 2)],
    p1_actions=[24, (24, 25), 26, (25, 26)],
):
    p0_color = game.state.colors[0]
    p1_color = game.state.colors[1]
    game.execute(Action(p0_color, ActionType.BUILD_SETTLEMENT, p0_actions[0]))
    game.execute(Action(p0_color, ActionType.BUILD_ROAD, p0_actions[1]))

    game.execute(Action(p1_color, ActionType.BUILD_SETTLEMENT, p1_actions[0]))
    game.execute(Action(p1_color, ActionType.BUILD_ROAD, p1_actions[1]))
    game.execute(Action(p1_color, ActionType.BUILD_SETTLEMENT, p1_actions[2]))
    game.execute(Action(p1_color, ActionType.BUILD_ROAD, p1_actions[3]))

    game.execute(Action(p0_color, ActionType.BUILD_SETTLEMENT, p0_actions[2]))
    game.execute(Action(p0_color, ActionType.BUILD_ROAD, p0_actions[3]))


def advance_to_play_turn(game):
    game.execute(Action(game.state.current_color(), ActionType.ROLL, None))
    while game.state.playable_actions[0].action_type in [
        ActionType.DISCARD,
        ActionType.MOVE_ROBBER,
    ]:
        game.execute(game.state.playable_actions[0])


def end_turn(game):
    game.execute(Action(game.state.current_color(), ActionType.END_TURN, None))


def continuous_roads_by_player(board, color: Color):
    paths = []
    components = board.find_connected_components(color)
    for component in components:
        paths.append(longest_acyclic_path(board, component, color))
    return paths
