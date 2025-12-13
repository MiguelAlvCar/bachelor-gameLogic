import numpy.typing as npt
import numpy as np
from typing import Callable, Awaitable, List

from logic.game.share.game_base import GameBase
from logic.game.comp_chasing_game.rules.unit_modificators_dict import unit_modificator_dict
from logic.map.geometry.directions import Directions
from logic.game.comp_chasing_game.exchange_position import exchange_positions
from logic.game.comp_chasing_game.change_position import change_position
from logic.game.comp_chasing_game.rules.general_rules import limit_organisation_retreat, limit_organisation_attack


async def combat(game: GameBase, own_unit_index: int, enemy_unit_index: int, is_red_command: bool, command_index: Directions,
                 friend_ocupied_fields: List[tuple[int, int]], enemy_ocupied_fields: List[tuple[int, int]], #dict[tuple[int, int], None],
                 on_finished: Callable[[float], Awaitable[None]]
           ) -> Awaitable[tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]]:
    if is_red_command:
        enemy_healths = game.blue_unit_healths
        friend_healths = game.red_unit_healths
        enemy_type = game.blue_unit_types[enemy_unit_index]
        friend_type = game.red_unit_types[own_unit_index]
        own_position = game.red_unit_positions[own_unit_index]
        enemy_position = game.blue_unit_positions[enemy_unit_index]
        enemy_positions = game.blue_unit_positions
        friend_positions = game.red_unit_positions
        map_enemy_positions = game.map.position_blue_units
        map_friend_positions = game.map.position_red_units
        enemy_terrain = game.map.terrain_types[enemy_position[0], enemy_position[1]]
        enemy_organisation = game.blue_unit_organization
        friend_organisation = game.red_unit_organization
    else:
        enemy_healths = game.red_unit_healths
        friend_healths = game.blue_unit_healths
        enemy_type = game.red_unit_types[enemy_unit_index]
        friend_type = game.blue_unit_types[own_unit_index]
        own_position = game.blue_unit_positions[own_unit_index]
        enemy_position = game.red_unit_positions[enemy_unit_index]
        enemy_terrain = game.map.terrain_types[enemy_position[0], enemy_position[1]]
        enemy_positions = game.red_unit_positions
        friend_positions = game.blue_unit_positions
        map_enemy_positions = game.map.position_red_units
        map_friend_positions = game.map.position_blue_units
        enemy_organisation = game.red_unit_organization
        friend_organisation = game.blue_unit_organization

    edited_enemies = [enemy_unit_index]

    own_unit_modificator = unit_modificator_dict[friend_type]
    enemy_unit_modificator = unit_modificator_dict[enemy_type]

    copy_organisation = enemy_organisation[enemy_unit_index].item()
    if copy_organisation < 0:
        copy_organisation = 0
    elif copy_organisation > limit_organisation_attack:
        copy_organisation = limit_organisation_attack
    copy_organisation = copy_organisation / limit_organisation_attack


    enemy_damage = (own_unit_modificator.strengh * 0.4 + own_unit_modificator.strengh * friend_healths[own_unit_index]  * 0.6) \
                    * own_unit_modificator.attack_terrain[enemy_terrain] \
                    * own_unit_modificator.attack_unit[enemy_type] * 0.87 / enemy_unit_modificator.defend_terrain[enemy_terrain]
    enemy_healths[enemy_unit_index] -= enemy_damage
    enemy_organisation[enemy_unit_index] -= enemy_damage * enemy_unit_modificator.organisation_vulnerability


    own_damage = (enemy_unit_modificator.strengh * 0.4 + enemy_unit_modificator.strengh * enemy_healths[enemy_unit_index] * 0.6) \
                    * copy_organisation \
                    * enemy_unit_modificator.attack_terrain[enemy_terrain] \
                    * enemy_unit_modificator.attack_unit[enemy_type]
    friend_healths[own_unit_index] -= own_damage
    friend_organisation[own_unit_index] -= own_damage * own_unit_modificator.organisation_vulnerability

    # retreat
    if enemy_organisation[enemy_unit_index] < limit_organisation_retreat * enemy_healths[enemy_unit_index]:
        is_retreating = False
        attack_target = enemy_positions[enemy_unit_index].copy()

        retreat_position_central = game.map.find_direction_field(command_index.value, enemy_position)
        retreat_position1 = game.map.find_direction_field((command_index.value + 1) % 6, enemy_position)
        retreat_position2 = game.map.find_direction_field((command_index.value - 1) % 6, enemy_position)

        friend_central = map_friend_positions[retreat_position_central[0], retreat_position_central[1]]
        friend1 = map_friend_positions[retreat_position1[0], retreat_position1[1]]
        friend2 = map_friend_positions[retreat_position2[0], retreat_position2[1]]

        friend_posibilities = np.array([friend1 == -1 and retreat_position1[0] != -1,
                                        friend_central == -1 and retreat_position_central[0] != -1,
                                        friend2 == -1 and retreat_position2[0] != -1,])

        sum = np.sum(friend_posibilities)

        if sum == 2:
            enemy_healths[enemy_unit_index] -= enemy_damage / 3
            enemy_organisation[enemy_unit_index] -= enemy_damage / 3 * enemy_unit_modificator.organisation_vulnerability
        elif sum == 1:
            enemy_healths[enemy_unit_index] -= enemy_damage
            enemy_organisation[enemy_unit_index] -= enemy_damage * enemy_unit_modificator.organisation_vulnerability
        elif sum == 0:
            enemy_healths[enemy_unit_index] = 0

        if enemy_healths[enemy_unit_index] > 0:
            enemy_central = map_enemy_positions[retreat_position_central[0], retreat_position_central[1]]
            enemy1 = map_enemy_positions[retreat_position1[0], retreat_position1[1]]
            enemy2 = map_enemy_positions[retreat_position2[0], retreat_position2[1]]
            enemies_posibilities = np.array([enemy1 == -1, enemy_central == -1, enemy2 == -1])

            if friend_posibilities.any():
                lateral_free_terrains = (friend_posibilities[[0,2]] & enemies_posibilities[[0,2]])
                if friend_posibilities[1]:
                    if enemies_posibilities[1]:
                        change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position_central,
                                        enemy_ocupied_fields, game.map.terrain_types)
                        is_retreating = True
                    else:
                        if lateral_free_terrains.any():
                            if np.sum(lateral_free_terrains) == 2:
                                x = np.random.randint(0, 6)
                                if x % 2 == 0:
                                    change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position1,
                                                    enemy_ocupied_fields, game.map.terrain_types)
                                    is_retreating = True
                                else:
                                    change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position2,
                                                    enemy_ocupied_fields, game.map.terrain_types)
                                    is_retreating = True
                            else:
                                if lateral_free_terrains[0]:
                                    change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position1,
                                                    enemy_ocupied_fields, game.map.terrain_types)
                                    is_retreating = True
                                else:
                                    change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position2,
                                                    enemy_ocupied_fields, game.map.terrain_types)
                                    is_retreating = True
                        else:
                            exchange_positions(enemy_unit_index, enemy_central, enemy_positions, map_enemy_positions)
                            edited_enemies.append(enemy_central)
                elif lateral_free_terrains.any():
                    if np.sum(lateral_free_terrains) == 2:
                        x = np.random.randint(0, 6)
                        if x % 2 == 0:
                            change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position1,
                                            enemy_ocupied_fields, game.map.terrain_types)
                            is_retreating = True
                        else:
                            change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position2,
                                            enemy_ocupied_fields, game.map.terrain_types)
                            is_retreating = True
                    else:
                        if lateral_free_terrains[0]:
                            change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position1,
                                            enemy_ocupied_fields, game.map.terrain_types)
                            is_retreating = True
                        else:
                            change_position(enemy_unit_index, enemy_positions, map_enemy_positions, retreat_position2,
                                            enemy_ocupied_fields, game.map.terrain_types)
                            is_retreating = True
                elif np.sum(enemies_posibilities[[0,2]]) == 0:
                    x = np.random.randint(0, 6)
                    if x % 2 == 0:
                        exchange_positions(enemy_unit_index, enemy1, enemy_positions, map_enemy_positions)
                        edited_enemies.append(enemy1)
                    else:
                        exchange_positions(enemy_unit_index, enemy2, enemy_positions, map_enemy_positions)
                        edited_enemies.append(enemy2)
                else:
                    if not enemies_posibilities[0]:
                        exchange_positions(enemy_unit_index, enemy1, enemy_positions, map_enemy_positions)
                        edited_enemies.append(enemy1)
                    else:
                        exchange_positions(enemy_unit_index, enemy2, enemy_positions, map_enemy_positions)
                        edited_enemies.append(enemy2)

        # pursue if retreating enemy
        if is_retreating:
            change_position(own_unit_index, friend_positions, map_friend_positions, attack_target,
                            friend_ocupied_fields, game.map.terrain_types)

    # pursue if dead enemy
    if enemy_healths[enemy_unit_index] <= 0:
        map_enemy_positions[enemy_position[0], enemy_position[1]] = -1
        change_position(own_unit_index, friend_positions, map_friend_positions, enemy_position,
                        friend_ocupied_fields, game.map.terrain_types)


    if friend_healths[own_unit_index] <= 0:
        map_friend_positions[own_position[0], own_position[1]] = -1


    if np.all(enemy_healths < 0.001):
        await _win(game, on_finished, is_red_command)
    elif np.all(friend_healths < 0.001):
        await _win(game, on_finished, not is_red_command)


    if is_red_command:
        return np.array([own_unit_index], dtype=np.int16), np.array(edited_enemies, dtype=np.int16)
    else:
        return np.array(edited_enemies, dtype=np.int16), np.array([own_unit_index], dtype=np.int16)

async def _win(game: GameBase, on_winning, is_red_win):
    if on_winning:
        await on_winning(game.is_red_turn)
    if is_red_win:
        game.result = 1
    else:
        game.result = 0
