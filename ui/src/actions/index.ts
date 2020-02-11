import {RepoActionTypes} from './repos'
import {JobActionTypes} from "./jobs";


type RootAction =
    | RepoActionTypes
    | JobActionTypes;

export default RootAction;