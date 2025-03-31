# Pokedex

## Objective

### Make a Pokedex style system (Pokemon encyclopedia) where you can search up pokemon and get its information, pulled straight from the PokeAPI API. DONE

### Pokemon pages contain:
    - Dex number DONE
    - Pokemon Name DONE
    - Generation Introduced DONE
    - Abilities DONE
    - Evolution line (As well as "links" to thos lines) NEEDS IMPROVEMENT
        -There are multiple cases where a pokemon evolution isn't directly 1->2->3 such as eevee which has 8 and wurmple which has 2 lines, need to account for all of these
        -Link hasnt been done yet
    - Stat total and individual stats DONE
    - Learnable moves DONE
    - Picture/Sprite/Visual Representation DONE
    - Misc info ie. Weight, Height, Gender distribution, etc. DONE*
        -More misc info can be added

## Extra Objectives

### Implement a search algorithm that gives 10 entries most similar to user input name if the spelling is wrong DONE*
    -Did 6 because it was easier to fit on the page

### Implement a filter system that allows a range of results based on Pokemon Type, Stat totals, Generation, etc. DONE*
    -Needs improvement because some pokemon have different forms, mega evolutions, etc, and these all have different names to differentiate them in the API which my basic implementation of interesection doesnt account for. So that needs to be improved on