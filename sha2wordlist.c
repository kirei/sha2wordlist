/*
 * Copyright (c) 2009 Kirei AB. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
 * IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
 * IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef __linux__
#include <bsd/string.h>
#endif

#include "sha2.h"

#define BUFLEN 16384

const char *wordlist_even[] = {
	"aardvark", "absurd", "accrue", "acme", "adrift",
	"adult", "afflict", "ahead", "aimless", "Algol",
	"allow", "alone", "ammo", "ancient", "apple",
	"artist", "assume", "Athens", "atlas", "Aztec",
	"baboon", "backfield", "backward", "banjo", "beaming",
	"bedlamp", "beehive", "beeswax", "befriend", "Belfast",
	"berserk", "billiard", "bison", "blackjack", "blockade",
	"blowtorch", "bluebird", "bombast", "bookshelf", "brackish",
	"breadline", "breakup", "brickyard", "briefcase", "Burbank",
	"button", "buzzard", "cement", "chairlift", "chatter",
	"checkup", "chisel", "choking", "chopper", "Christmas",
	"clamshell", "classic", "classroom", "cleanup", "clockwork",
	"cobra", "commence", "concert", "cowbell", "crackdown",
	"cranky", "crowfoot", "crucial", "crumpled", "crusade",
	"cubic", "dashboard", "deadbolt", "deckhand", "dogsled",
	"dragnet", "drainage", "dreadful", "drifter", "dropper",
	"drumbeat", "drunken", "Dupont", "dwelling", "eating",
	"edict", "egghead", "eightball", "endorse", "endow",
	"enlist", "erase", "escape", "exceed", "eyeglass",
	"eyetooth", "facial", "fallout", "flagpole", "flatfoot",
	"flytrap", "fracture", "framework", "freedom", "frighten",
	"gazelle", "Geiger", "glitter", "glucose", "goggles",
	"goldfish", "gremlin", "guidance", "hamlet", "highchair",
	"hockey", "indoors", "indulge", "inverse", "involve",
	"island", "jawbone", "keyboard", "kickoff", "kiwi",
	"klaxon", "locale", "lockup", "merit", "minnow",
	"miser", "Mohawk", "mural", "music", "necklace",
	"Neptune", "newborn", "nightbird", "Oakland", "obtuse",
	"offload", "optic", "orca", "payday", "peachy",
	"pheasant", "physique", "playhouse", "Pluto", "preclude",
	"prefer", "preshrunk", "printer", "prowler", "pupil",
	"puppy", "python", "quadrant", "quiver", "quota",
	"ragtime", "ratchet", "rebirth", "reform", "regain",
	"reindeer", "rematch", "repay", "retouch", "revenge",
	"reward", "rhythm", "ribcage", "ringbolt", "robust",
	"rocker", "ruffled", "sailboat", "sawdust", "scallion",
	"scenic", "scorecard", "Scotland", "seabird", "select",
	"sentence", "shadow", "shamrock", "showgirl", "skullcap",
	"skydive", "slingshot", "slowdown", "snapline", "snapshot",
	"snowcap", "snowslide", "solo", "southward", "soybean",
	"spaniel", "spearhead", "spellbind", "spheroid", "spigot",
	"spindle", "spyglass", "stagehand", "stagnate", "stairway",
	"standard", "stapler", "steamship", "sterling", "stockman",
	"stopwatch", "stormy", "sugar", "surmount", "suspense",
	"sweatband", "swelter", "tactics", "talon", "tapeworm",
	"tempest", "tiger", "tissue", "tonic", "topmost",
	"tracker", "transit", "trauma", "treadmill", "Trojan",
	"trouble", "tumor", "tunnel", "tycoon", "uncut",
	"unearth", "unwind", "uproot", "upset", "upshot",
	"vapor", "village", "virus", "Vulcan", "waffle",
	"wallet", "watchword", "wayside", "willow", "woodlark",
	"Zulu"
};

const char *wordlist_odd[] = {
	"adroitness", "adviser", "aftermath", "aggregate", "alkali",
	"almighty", "amulet", "amusement", "antenna", "applicant",
	"Apollo", "armistice", "article", "asteroid", "Atlantic",
	"atmosphere", "autopsy", "Babylon", "backwater", "barbecue",
	"belowground", "bifocals", "bodyguard", "bookseller",
	"borderline", "bottomless", "Bradbury", "bravado",
	"Brazilian", "breakaway", "Burlington", "businessman",
	"butterfat", "Camelot", "candidate", "cannonball",
	"Capricorn", "caravan", "caretaker", "celebrate",
	"cellulose", "certify", "chambermaid", "Cherokee",
	"Chicago", "clergyman", "coherence", "combustion",
	"commando", "company", "component", "concurrent",
	"confidence", "conformist", "congregate", "consensus",
	"consulting", "corporate", "corrosion", "councilman",
	"crossover", "crucifix", "cumbersome", "customer", "Dakota",
	"decadence", "December", "decimal", "designing", "detector",
	"detergent", "determine", "dictator", "dinosaur",
	"direction", "disable", "disbelief", "disruptive",
	"distortion", "document", "embezzle", "enchanting",
	"enrollment", "enterprise", "equation", "equipment",
	"escapade", "Eskimo", "everyday", "examine", "existence",
	"exodus", "fascinate", "filament", "finicky", "forever",
	"fortitude", "frequency", "gadgetry", "Galveston",
	"getaway", "glossary", "gossamer", "graduate", "gravity",
	"guitarist", "hamburger", "Hamilton", "handiwork",
	"hazardous", "headwaters", "hemisphere", "hesitate",
	"hideaway", "holiness", "hurricane", "hydraulic",
	"impartial", "impetus", "inception", "indigo", "inertia",
	"infancy", "inferno", "informant", "insincere", "insurgent",
	"integrate", "intention", "inventive", "Istanbul",
	"Jamaica", "Jupiter", "leprosy", "letterhead", "liberty",
	"maritime", "matchmaker", "maverick", "Medusa", "megaton",
	"microscope", "microwave", "midsummer", "millionaire",
	"miracle", "misnomer", "molasses", "molecule", "Montana",
	"monument", "mosquito", "narrative", "nebula", "newsletter",
	"Norwegian", "October", "Ohio", "onlooker", "opulent",
	"Orlando", "outfielder", "Pacific", "pandemic", "Pandora",
	"paperweight", "paragon", "paragraph", "paramount",
	"passenger", "pedigree", "Pegasus", "penetrate",
	"perceptive", "performance", "pharmacy", "phonetic",
	"photograph", "pioneer", "pocketful", "politeness",
	"positive", "potato", "processor", "provincial",
	"proximate", "puberty", "publisher", "pyramid", "quantity",
	"racketeer", "rebellion", "recipe", "recover", "repellent",
	"replica", "reproduce", "resistor", "responsive",
	"retraction", "retrieval", "retrospect", "revenue",
	"revival", "revolver", "sandalwood", "sardonic", "Saturday",
	"savagery", "scavenger", "sensation", "sociable",
	"souvenir", "specialist", "speculate", "stethoscope",
	"stupendous", "supportive", "surrender", "suspicious",
	"sympathy", "tambourine", "telephone", "therapist",
	"tobacco", "tolerance", "tomorrow", "torpedo", "tradition",
	"travesty", "trombonist", "truncated", "typewriter",
	"ultimate", "undaunted", "underfoot", "unicorn", "unify",
	"universe", "unravel", "upcoming", "vacancy", "vagabond",
	"vertigo", "Virginia", "visitor", "vocalist", "voyager",
	"warranty", "Waterloo", "whimsical", "Wichita",
	"Wilmington", "Wyoming", "yesteryear", "Yucatan"
};

int
hex2int(char hc)
{
	if (hc >= '0' && hc <= '9')
		return hc - '0';
	if (hc >= 'A' && hc <= 'F')
		return hc - 'A' + 10;
	if (hc >= 'a' && hc <= 'f')
		return hc - 'a' + 10;
	return 0;
}

void
pgp_wordlist(const char *str, char *buf, size_t bufsize)
{
	int i;
	int b;
	size_t nwords;

	nwords = strlen(str) / 2;
	buf[0] = '\0';
	
	for (i = 0; i < nwords; i++) {
		b = (hex2int(str[i*2]) << 4) + hex2int(str[i*2+1]);
		if (i % 2)
			strlcat(buf, wordlist_odd[b], bufsize);
		else
			strlcat(buf, wordlist_even[b], bufsize);
		if (i != nwords-1)
			strlcat(buf, " ", bufsize);
	}
}

int
main(int argc, char **argv)
{
	int fd;
	ssize_t nbytes;
	SHA256_CTX ctx256;
	char hash[BUFLEN];
	char words[BUFLEN];

	fd = fileno(stdin);

	SHA256_Init(&ctx256);

	while ((nbytes = read(fd, hash, BUFLEN)) > 0)
		SHA256_Update(&ctx256, (unsigned char *) hash, nbytes);

	SHA256_End(&ctx256, hash);
	
	pgp_wordlist(hash, words, sizeof(words));

	printf("SHA-256:    %s\n",  hash);
	printf("PGP Words:  %s\n", words);

	exit(0);
}
