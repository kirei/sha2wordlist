"""
Copyright (c) 2009 Kirei AB. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import hashlib
import sys
from typing import List

BUFLEN = 16384

# https://en.wikipedia.org/wiki/PGP_word_list
# https://philzimmermann.com/docs/PGP_word_list.pdf
WORDS = [
    ("aardvark", "adroitness"),
    ("absurd", "adviser"),
    ("accrue", "aftermath"),
    ("acme", "aggregate"),
    ("adrift", "alkali"),
    ("adult", "almighty"),
    ("afflict", "amulet"),
    ("ahead", "amusement"),
    ("aimless", "antenna"),
    ("Algol", "applicant"),
    ("allow", "Apollo"),
    ("alone", "armistice"),
    ("ammo", "article"),
    ("ancient", "asteroid"),
    ("apple", "Atlantic"),
    ("artist", "atmosphere"),
    ("assume", "autopsy"),
    ("Athens", "Babylon"),
    ("atlas", "backwater"),
    ("Aztec", "barbecue"),
    ("baboon", "belowground"),
    ("backfield", "bifocals"),
    ("backward", "bodyguard"),
    ("banjo", "bookseller"),
    ("beaming", "borderline"),
    ("bedlamp", "bottomless"),
    ("beehive", "Bradbury"),
    ("beeswax", "bravado"),
    ("befriend", "Brazilian"),
    ("Belfast", "breakaway"),
    ("berserk", "Burlington"),
    ("billiard", "businessman"),
    ("bison", "butterfat"),
    ("blackjack", "Camelot"),
    ("blockade", "candidate"),
    ("blowtorch", "cannonball"),
    ("bluebird", "Capricorn"),
    ("bombast", "caravan"),
    ("bookshelf", "caretaker"),
    ("brackish", "celebrate"),
    ("breadline", "cellulose"),
    ("breakup", "certify"),
    ("brickyard", "chambermaid"),
    ("briefcase", "Cherokee"),
    ("Burbank", "Chicago"),
    ("button", "clergyman"),
    ("buzzard", "coherence"),
    ("cement", "combustion"),
    ("chairlift", "commando"),
    ("chatter", "company"),
    ("checkup", "component"),
    ("chisel", "concurrent"),
    ("choking", "confidence"),
    ("chopper", "conformist"),
    ("Christmas", "congregate"),
    ("clamshell", "consensus"),
    ("classic", "consulting"),
    ("classroom", "corporate"),
    ("cleanup", "corrosion"),
    ("clockwork", "councilman"),
    ("cobra", "crossover"),
    ("commence", "crucifix"),
    ("concert", "cumbersome"),
    ("cowbell", "customer"),
    ("crackdown", "Dakota"),
    ("cranky", "decadence"),
    ("crowfoot", "December"),
    ("crucial", "decimal"),
    ("crumpled", "designing"),
    ("crusade", "detector"),
    ("cubic", "detergent"),
    ("dashboard", "determine"),
    ("deadbolt", "dictator"),
    ("deckhand", "dinosaur"),
    ("dogsled", "direction"),
    ("dragnet", "disable"),
    ("drainage", "disbelief"),
    ("dreadful", "disruptive"),
    ("drifter", "distortion"),
    ("dropper", "document"),
    ("drumbeat", "embezzle"),
    ("drunken", "enchanting"),
    ("Dupont", "enrollment"),
    ("dwelling", "enterprise"),
    ("eating", "equation"),
    ("edict", "equipment"),
    ("egghead", "escapade"),
    ("eightball", "Eskimo"),
    ("endorse", "everyday"),
    ("endow", "examine"),
    ("enlist", "existence"),
    ("erase", "exodus"),
    ("escape", "fascinate"),
    ("exceed", "filament"),
    ("eyeglass", "finicky"),
    ("eyetooth", "forever"),
    ("facial", "fortitude"),
    ("fallout", "frequency"),
    ("flagpole", "gadgetry"),
    ("flatfoot", "Galveston"),
    ("flytrap", "getaway"),
    ("fracture", "glossary"),
    ("framework", "gossamer"),
    ("freedom", "graduate"),
    ("frighten", "gravity"),
    ("gazelle", "guitarist"),
    ("Geiger", "hamburger"),
    ("glitter", "Hamilton"),
    ("glucose", "handiwork"),
    ("goggles", "hazardous"),
    ("goldfish", "headwaters"),
    ("gremlin", "hemisphere"),
    ("guidance", "hesitate"),
    ("hamlet", "hideaway"),
    ("highchair", "holiness"),
    ("hockey", "hurricane"),
    ("indoors", "hydraulic"),
    ("indulge", "impartial"),
    ("inverse", "impetus"),
    ("involve", "inception"),
    ("island", "indigo"),
    ("jawbone", "inertia"),
    ("keyboard", "infancy"),
    ("kickoff", "inferno"),
    ("kiwi", "informant"),
    ("klaxon", "insincere"),
    ("locale", "insurgent"),
    ("lockup", "integrate"),
    ("merit", "intention"),
    ("minnow", "inventive"),
    ("miser", "Istanbul"),
    ("Mohawk", "Jamaica"),
    ("mural", "Jupiter"),
    ("music", "leprosy"),
    ("necklace", "letterhead"),
    ("Neptune", "liberty"),
    ("newborn", "maritime"),
    ("nightbird", "matchmaker"),
    ("Oakland", "maverick"),
    ("obtuse", "Medusa"),
    ("offload", "megaton"),
    ("optic", "microscope"),
    ("orca", "microwave"),
    ("payday", "midsummer"),
    ("peachy", "millionaire"),
    ("pheasant", "miracle"),
    ("physique", "misnomer"),
    ("playhouse", "molasses"),
    ("Pluto", "molecule"),
    ("preclude", "Montana"),
    ("prefer", "monument"),
    ("preshrunk", "mosquito"),
    ("printer", "narrative"),
    ("prowler", "nebula"),
    ("pupil", "newsletter"),
    ("puppy", "Norwegian"),
    ("python", "October"),
    ("quadrant", "Ohio"),
    ("quiver", "onlooker"),
    ("quota", "opulent"),
    ("ragtime", "Orlando"),
    ("ratchet", "outfielder"),
    ("rebirth", "Pacific"),
    ("reform", "pandemic"),
    ("regain", "Pandora"),
    ("reindeer", "paperweight"),
    ("rematch", "paragon"),
    ("repay", "paragraph"),
    ("retouch", "paramount"),
    ("revenge", "passenger"),
    ("reward", "pedigree"),
    ("rhythm", "Pegasus"),
    ("ribcage", "penetrate"),
    ("ringbolt", "perceptive"),
    ("robust", "performance"),
    ("rocker", "pharmacy"),
    ("ruffled", "phonetic"),
    ("sailboat", "photograph"),
    ("sawdust", "pioneer"),
    ("scallion", "pocketful"),
    ("scenic", "politeness"),
    ("scorecard", "positive"),
    ("Scotland", "potato"),
    ("seabird", "processor"),
    ("select", "provincial"),
    ("sentence", "proximate"),
    ("shadow", "puberty"),
    ("shamrock", "publisher"),
    ("showgirl", "pyramid"),
    ("skullcap", "quantity"),
    ("skydive", "racketeer"),
    ("slingshot", "rebellion"),
    ("slowdown", "recipe"),
    ("snapline", "recover"),
    ("snapshot", "repellent"),
    ("snowcap", "replica"),
    ("snowslide", "reproduce"),
    ("solo", "resistor"),
    ("southward", "responsive"),
    ("soybean", "retraction"),
    ("spaniel", "retrieval"),
    ("spearhead", "retrospect"),
    ("spellbind", "revenue"),
    ("spheroid", "revival"),
    ("spigot", "revolver"),
    ("spindle", "sandalwood"),
    ("spyglass", "sardonic"),
    ("stagehand", "Saturday"),
    ("stagnate", "savagery"),
    ("stairway", "scavenger"),
    ("standard", "sensation"),
    ("stapler", "sociable"),
    ("steamship", "souvenir"),
    ("sterling", "specialist"),
    ("stockman", "speculate"),
    ("stopwatch", "stethoscope"),
    ("stormy", "stupendous"),
    ("sugar", "supportive"),
    ("surmount", "surrender"),
    ("suspense", "suspicious"),
    ("sweatband", "sympathy"),
    ("swelter", "tambourine"),
    ("tactics", "telephone"),
    ("talon", "therapist"),
    ("tapeworm", "tobacco"),
    ("tempest", "tolerance"),
    ("tiger", "tomorrow"),
    ("tissue", "torpedo"),
    ("tonic", "tradition"),
    ("topmost", "travesty"),
    ("tracker", "trombonist"),
    ("transit", "truncated"),
    ("trauma", "typewriter"),
    ("treadmill", "ultimate"),
    ("Trojan", "undaunted"),
    ("trouble", "underfoot"),
    ("tumor", "unicorn"),
    ("tunnel", "unify"),
    ("tycoon", "universe"),
    ("uncut", "unravel"),
    ("unearth", "upcoming"),
    ("unwind", "vacancy"),
    ("uproot", "vagabond"),
    ("upset", "vertigo"),
    ("upshot", "Virginia"),
    ("vapor", "visitor"),
    ("village", "vocalist"),
    ("virus", "voyager"),
    ("Vulcan", "warranty"),
    ("waffle", "Waterloo"),
    ("wallet", "whimsical"),
    ("watchword", "Wichita"),
    ("wayside", "Wilmington"),
    ("willow", "Wyoming"),
    ("woodlark", "yesteryear"),
    ("Zulu", "Yucatan"),
]


def pgp_wordlist(data: bytes) -> List[str]:
    """Translate bytes to list of PGP words."""
    odd = False
    words = []
    for byte in data:
        if odd:
            words.append(WORDS[byte][1])
        else:
            words.append(WORDS[byte][0])
        odd = not odd
    return words


def main() -> None:
    """Main function"""
    h = hashlib.new("sha256")

    while data:
        data = sys.stdin.buffer.read(BUFLEN)
        if data:
            h.update(data)
        else:
            break

    words = " ".join(pgp_wordlist(h.digest()))
    print("SHA-256:    ", h.hexdigest())
    print("PGP Words:  ", words)


if __name__ == "__main__":
    main()
