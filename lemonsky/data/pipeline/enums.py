# from enum import StrEnum


class ContentTypeEnums():
    Season = "season"
    Episode = "episode"
    Sequence = "sequence"
    Shot = "shot"
    Asset = "asset"
    Motion = "motion"

    def label(self) -> str:
        labels = {
            ContentTypeEnums.Episode: "Episode",
            ContentTypeEnums.Season: "Season",
            ContentTypeEnums.Sequence: "Sequence",
            ContentTypeEnums.Shot: "Shot",
            ContentTypeEnums.Asset: "Asset",
            ContentTypeEnums.Motion: "Motion",
        }
        return labels[self]


class ContentCategory():
    Marketing = "Marketing"
    Concept = "Concept"
    Graphics = "Graphics"
    PrePro = "PrePro"
    Asset = "Asset"
    Animation = "Animation"


class ContentCategoryType():
    Poster = "Poster"
    BreakdownVideo = "BreakdownVideo"
    KeyArt = "KeyArt"
    Character = "Character"
    Set = "Set"
    Prop = "Prop"
    Transportation = "Transportation"
    ColorKey = "ColorKey"
    Avatar = "Avatar"
    Logo = "Logo"
    BG = "BG"
    Storyboard = "Storyboard"
    Animatic = "Animatic"
    Previz = "Previz"
    CrowdAnim = "CrowdAnim"
    FX = "FX"
    Groom = "Groom"
    ClothSU = "ClothSU"
    Light = "Light"
    CYC = "CYC"
    Cuts = "Cuts"
    Motions = "Motions"
    LineUp = "LineUp"


class ProjectDivision():
    ANIMATION = "animation"
    GAME = "game"

    def label(self) -> str:
        labels = {
            ProjectDivision.ANIMATION: "Animation",
            ProjectDivision.GAME: "Game",
        }
        return labels[self]


class ProjectStage():
    NEW = "new"
    INPROGRESS = "inprogress"
    ONHOLD = "onhold"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ARCHIVED = "archived"

    def label(self) -> str:
        labels = {
            ProjectStage.NEW: "New",
            ProjectStage.INPROGRESS: "In Progress",
            ProjectStage.ONHOLD: "On Hold",
            ProjectStage.CANCELLED: "Cancelled",
            ProjectStage.COMPLETED: "Completed",
            ProjectStage.ARCHIVED: "Archived",
        }
        return labels[self]


class ProjectType():
    ADVERTISEMENT = "advertisement"
    GAME = "game"
    GAME_ANIM = "game_animation"
    TV = "tv"
    FILM = "film"
    DEMO = "demo"

    def label(self) -> str:
        labels = {
            ProjectType.ADVERTISEMENT: "Advertisement",
            ProjectType.GAME: "Game",
            ProjectType.GAME_ANIM: "Game Animation",
            ProjectType.TV: "TV",
            ProjectType.FILM: "Film",
            ProjectType.DEMO: "Demo",
        }
        return labels[self]


class TaskPriority():
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def label(self) -> str:
        labels = {
            TaskPriority.LOW: "Low",
            TaskPriority.MEDIUM: "Medium",
            TaskPriority.HIGH: "High",
        }
        return labels[self]


class TaskStatus():
    NEW = "new"
    WIP = "wip"
    PUB = "pub"

    def label(self) -> str:
        labels = {
            TaskStatus.NEW: "New",
            TaskStatus.WIP: "WIP",
            TaskStatus.PUB: "Published",
        }
        return labels[self]
