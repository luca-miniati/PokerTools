import toml from 'toml';

export type Suit = 'c' | 'd' | 'h' | 's';
export type Rank = '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'T' | 'J' | 'Q' | 'K' | 'A';
export const RANKS: Rank[] = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
const NUM_COMBOS = 1326;  // 52C2

export type Action = {
    name: string;
    amount?: number;
}

export type HandAction = {
    action: Action;
    freq: number;
}

const RANGES = {
  utg_rfi_30bb: () => import('$lib/assets/ranges/utg_rfi_30bb.toml?raw'),
  utg1_rfi_30bb: () => import('$lib/assets/ranges/utg1_rfi_30bb.toml?raw'),
  mp_rfi_30bb: () => import('$lib/assets/ranges/mp_rfi_30bb.toml?raw'),
  hj_rfi_30bb: () => import('$lib/assets/ranges/hj_rfi_30bb.toml?raw'),
  co_rfi_30bb: () => import('$lib/assets/ranges/co_rfi_30bb.toml?raw'),
  btn_rfi_30bb: () => import('$lib/assets/ranges/btn_rfi_30bb.toml?raw'),
  sb_rfi_30bb: () => import('$lib/assets/ranges/sb_rfi_30bb.toml?raw'),
};

export type RangeKey = keyof typeof RANGES;
export const Ranges = Object.keys(RANGES);
export const Positions = [
    'SB',
    'BB',
    'UTG',
    'UTG1',
    'MP',
    'HJ',
    'CO',
    'BTN',
];
export const Actions = [
    'RFI',
];
export const StackSizes = [
    '30bb',
];


export class Range {
    position: string;
    action: string;
    stackSize: string;
    strategy: Record<string, HandAction[]> = {};

    private constructor(position: string, action: string, stackSize: string, strategy: Record<string, HandAction[]>) {
        this.position = position;
        this.action = action;
        this.stackSize = stackSize;
        this.strategy = strategy;
    }

    static parseStrategy(data: Record<string, any>): Record<string, HandAction[]> {
        return Object.fromEntries(
            Object.entries(data)
                .filter(([hand]) => hand !== 'meta')
                .map(([hand, actions]) => [
                    hand,
                    actions.map((a: any) => ({
                        action: { name: a.action, amount: a.amount },
                        freq: a.freq
                    }))
                ])
        );
    }

    static async create(name: RangeKey): Promise<Range> {
        const module = await RANGES[name]();
        const text = module.default;
        const data = toml.parse(text) as Record<string, any>;
        return new Range(
            data['meta']['position'],
            data['meta']['action'],
            data['meta']['stack'],
            this.parseStrategy(data),
        );
    }

    getName(): string {
        return this.stackSize + ' ' + this.position + ' ' + this.action
    }

    get(hand: string): HandAction[] {
        return this.strategy[hand];
    }

    getNumCombos(hand: string): number {
        const last = hand[hand.length - 1];
        switch (last) {
            case 's':  // suited
                return 4;
            case 'o':  // offfsuit
                return 16;
            default:  // pocket pair
                return 6;
        }
    }

    getActions(): Set<Action> {
        let actions: Set<Action> = new Set<Action>();

        for (const handActions of Object.values(this.strategy))
            for (const { action, freq } of handActions)
                actions.add(action);

        return actions;
    }


    getAggregateStrategy(): Record<string, number> {
        let strategy: Record<string, number> = {};

        for (const [hand, handActions] of Object.entries(this.strategy)) {
            const numCombos: number = this.getNumCombos(hand);
            for (const { action, freq } of handActions) {
                const { name, amount } = action;
                const actionString = `${name}${amount ? ' ' + amount + 'bb' : ''}`;

                strategy[actionString] = (strategy[actionString] ?? 0.0) + freq * numCombos;
            }
        }

        for (const actionString in strategy)
            strategy[actionString] /= NUM_COMBOS;

        return strategy;
    }

    // encodeHands(hands: string[], action: Action): string {
    //     let res = '';
        
    //     let curr: string[] = [];
    //     for (const hand of hands) {
    //         if (this.strategy[hand].includes(action))
    //     }

    //     return res;
    // }

    // encode(): string {
    //     let res: Record<
    //         string,
    //         string | Record<
    //             string, string | number
    //         >[]
    //     > = {};

    //     res['name']         = this.getName();
    //     res['stack']        = this.stackSize;
    //     res['position']     = this.position;
    //     res['action']       = this.action;
    //     res['range']        = [];

    //     for (const action of this.getActions()) {
    //         let range: Record<string, string | number> = {};
    //         range['action'] = action.name;
    //         if (action.amount)
    //             range['amount'] = action.amount;
    //         range['hands'] = '';

    //         // Pocket pairs
    //         range['hands'] += this.encodeHands(
    //             RANKS.map((r) => r + r),
    //             action,
    //         );

    //         let offsuitCombos = [];
    //         let suitedCombos = [];
    //         for (const r1 of RANKS) {
    //             for (const r2 of RANKS) {
    //                 if (RANKS.indexOf(r1) < RANKS.indexOf(r2)) {
    //                     offsuitCombos.push(r1 + r2 + 'o');
    //                     suitedCombos.push(r1 + r2 + 's');
    //                 }
    //             }
    //         }

    //         range['hands'] += this.encodeHands(
    //             offsuitCombos,
    //             action
    //         );

    //         range['hands'] += this.encodeHands(
    //             suitedCombos,
    //             action
    //         );
    //     }

    //     return JSON.stringify(res);
    // }
}
